import warnings
import torch
from tabensemb.utils import *
from tabensemb.model import AbstractModel
from skopt.space import Integer, Real, Categorical
import shutil
import numpy as np
from pytorch_lightning import Callback
import pytorch_lightning as pl
from .base import PytorchLightningLossCallback
from .base import AbstractWrapper
from typing import Dict, Any
from packaging import version
from torch import nn
import re
import inspect


class PytorchTabular(AbstractModel):
    def _get_program_name(self):
        return "PytorchTabular"

    def _new_model(self, model_name, verbose, **kwargs):
        warnings.filterwarnings("ignore", message="Wandb")
        from ._pytorch_tabular.mute_track import mute_track

        mute_track()

        from functools import partialmethod
        import pytorch_tabular
        from pytorch_tabular.config import ExperimentRunManager

        erm_original_init = ExperimentRunManager.__init__
        ExperimentRunManager.__init__ = partialmethod(
            ExperimentRunManager.__init__,
            exp_version_manager=os.path.join(self.root, "exp_version_manager.yml"),
        )
        from pytorch_tabular import TabularModel
        from pytorch_tabular.models import (
            CategoryEmbeddingModelConfig,
            NodeConfig,
            TabNetModelConfig,
            TabTransformerConfig,
            AutoIntConfig,
            FTTransformerConfig,
            GatedAdditiveTreeEnsembleConfig,
        )
        from pytorch_tabular.config import DataConfig, OptimizerConfig, TrainerConfig

        task = self.trainer.datamodule.task
        self.task = task
        if task in ["binary", "multiclass"]:
            task = "classification"
        loss = self.trainer.datamodule.loss
        mapping = {
            "cross_entropy": "CrossEntropyLoss",
            "mse": "MSELoss",
            "mae": "L1Loss",
        }
        if loss in mapping.keys():
            loss = mapping[loss]
        self.loss = loss

        data_config = DataConfig(
            target=self.trainer.label_name,
            continuous_cols=self.trainer.cont_feature_names,
            categorical_cols=self.trainer.cat_feature_names,
            num_workers=0,
        )
        if not os.path.exists(os.path.join(self.root, "ckpts")):
            os.mkdir(os.path.join(self.root, "ckpts"))
        trainer_config = TrainerConfig(
            batch_size=int(kwargs["batch_size"]),
            progress_bar="none",
            early_stopping="valid_loss",
            early_stopping_patience=self.trainer.static_params["patience"],
            checkpoints="valid_loss",
            checkpoints_path=os.path.join(self.root, "ckpts"),
            checkpoints_save_top_k=1,
            checkpoints_name=model_name,
            load_best=True,
            accelerator="cpu" if self.device == "cpu" else "auto",
        )
        (
            opt_name,
            opt_params,
            lrs_name,
            lrs_params,
        ) = self._update_optimizer_lr_scheduler_params(model_name=model_name, **kwargs)
        if "lr" in opt_params.keys():
            # pytorch_tabular deals with the learning rate individually.
            del opt_params["lr"]
        optimizer_config = OptimizerConfig(
            optimizer=opt_name,
            optimizer_params=opt_params,
            lr_scheduler=lrs_name,
            lr_scheduler_params=lrs_params,
        )

        model_configs = {
            "Category Embedding": CategoryEmbeddingModelConfig,
            "NODE": NodeConfig,
            "TabNet": TabNetModelConfig,
            "TabTransformer": TabTransformerConfig,
            "AutoInt": AutoIntConfig,
            "FTTransformer": FTTransformerConfig,
            "GATE": GatedAdditiveTreeEnsembleConfig,
        }
        special_configs = {
            "NODE": (
                {"embed_categorical": True}
                if version.parse(pytorch_tabular.__version__) < version.parse("1.1.0")
                else {}
            ),
        }
        legal_kwargs = {
            key: value
            for key, value in kwargs.items()
            if key not in ["lr", "batch_size", "original_batch_size"]
            and key not in opt_params.keys()
            and key not in lrs_params.keys()
        }
        if "lr" in kwargs.keys():
            legal_kwargs["learning_rate"] = kwargs["lr"]
        for key in legal_kwargs.keys():
            if type(legal_kwargs[key]) in [np.str_, np.int_]:
                try:
                    legal_kwargs[key] = int(legal_kwargs[key])
                except:
                    pass
        with HiddenPrints():
            model_config = (
                model_configs[model_name](task=task, loss=loss, **legal_kwargs)
                if model_name not in special_configs.keys()
                else model_configs[model_name](
                    task=task, loss=loss, **special_configs[model_name], **legal_kwargs
                )
            )
            tabular_model = TabularModel(
                data_config=data_config,
                model_config=model_config,
                optimizer_config=optimizer_config,
                trainer_config=trainer_config,
            )
            tabular_model.logger = False
        tabular_model.config["progress_bar_refresh_rate"] = 0
        ExperimentRunManager.__init__ = erm_original_init
        return tabular_model

    def _train_data_preprocess(self, model_name, warm_start=False):
        data = self.trainer.datamodule
        all_feature_names = self.trainer.all_feature_names
        X_train = data.categories_inverse_transform(data.X_train)[all_feature_names]
        X_val = data.categories_inverse_transform(data.X_val)[all_feature_names]
        X_test = data.categories_inverse_transform(data.X_test)[all_feature_names]
        return {
            "X_train": X_train,
            "y_train": data.y_train,
            "X_val": X_val,
            "y_val": data.y_val,
            "X_test": X_test,
            "y_test": data.y_test,
        }

    def _data_preprocess(self, df, derived_data, model_name):
        all_feature_names = self.trainer.all_feature_names
        df = self.trainer.datamodule.categories_inverse_transform(df.copy())[
            all_feature_names
        ]
        return df

    def _train_single_model(
        self,
        model,
        model_name,
        epoch,
        X_train,
        y_train,
        X_val,
        y_val,
        verbose,
        warm_start,
        in_bayes_opt,
        **kwargs,
    ):
        tc = TqdmController()
        tc.disable_tqdm()
        label_name = self.trainer.label_name
        train_data = X_train.copy()
        train_data[label_name] = y_train
        val_data = X_val.copy()
        val_data[label_name] = y_val
        pl_loss_callback = PytorchLightningLossCallback(
            verbose=verbose, total_epoch=epoch
        )
        with HiddenPrints(
            disable_std=not verbose,
            disable_logging=not verbose,
        ):
            with warnings.catch_warnings():
                from pytorch_lightning.utilities.rank_zero import (
                    LightningDeprecationWarning,
                )

                warnings.filterwarnings("ignore", category=LightningDeprecationWarning)
                warnings.simplefilter(action="ignore", category=UserWarning)
                model.fit(
                    train=train_data,
                    validation=val_data,
                    max_epochs=epoch,
                    callbacks=[
                        PytorchTabularVerboseLossCallback(),
                        pl_loss_callback,
                    ],
                )
        self.train_losses[model_name] = pl_loss_callback.train_ls
        self.val_losses[model_name] = pl_loss_callback.val_ls

        from pytorch_lightning.callbacks import ModelCheckpoint

        ckpt_callback = None
        for callback in model.callbacks:
            if isinstance(callback, ModelCheckpoint):
                ckpt_callback = callback
                break
        if ckpt_callback is not None:
            self.restored_epochs[model_name] = int(
                re.findall(r"epoch=([0-9]*)-", ckpt_callback.kth_best_model_path)[0]
            )
        if os.path.exists(os.path.join(self.root, "ckpts")):
            shutil.rmtree(os.path.join(self.root, "ckpts"))
        tc.enable_tqdm()

    def _pred_single_model(self, model, X_test, verbose, **kwargs):
        from ._pytorch_tabular.mute_track import mute_track

        mute_track()
        targets = model.config.target
        with HiddenPrints():
            # Two annoying warnings that cannot be suppressed:
            # 1. DeprecationWarning: Default for ``include_input_features`` will change from True to False in the next
            # release. Please set it explicitly.
            # 2. DeprecationWarning: "The ``out_ff_layers``, ``out_ff_activation``, ``out_ff_dropoout``, and
            # ``out_ff_initialization`` arguments are deprecated and will be removed next release. Please use head and
            # head_config as an alternative.
            original_batch_size = model.datamodule.batch_size
            model.datamodule.batch_size = len(X_test)
            warnings.filterwarnings(
                "ignore", category=DeprecationWarning, module="pytorch_tabular"
            )
            all_res = model.predict(X_test, include_input_features=False)
            model.datamodule.batch_size = original_batch_size
            if self.task == "regression":
                preds = [
                    np.array(all_res[f"{target}_prediction"]).reshape(-1, 1)
                    for target in targets
                ]
                res = np.concatenate(preds, axis=1)
            elif self.task == "binary":
                res = np.array(all_res[f"1_probability"]).reshape(-1, 1)
            else:
                n_classes = len(all_res.columns) - 1
                res = np.array(all_res)[:, :n_classes]
        return res

    @staticmethod
    def _get_model_names():
        return [
            "Category Embedding",
            "NODE",
            "TabNet",
            "TabTransformer",
            "AutoInt",
            "FTTransformer",
            # "GATE", Low efficiency
        ]

    def _space(self, model_name):
        """
        Spaces are selected around default parameters.
        """
        space_dict = {
            "Category Embedding": [
                Real(low=0, high=0.5, prior="uniform", name="dropout"),  # 0.5
                Real(low=0, high=0.5, prior="uniform", name="embedding_dropout"),  # 0.5
            ]
            + self.trainer.SPACE,
            "NODE": [
                Integer(low=2, high=5, prior="uniform", name="depth", dtype=int),  # 6
                Real(low=0, high=0.3, prior="uniform", name="embedding_dropout"),  # 0.0
                Real(low=0, high=0.3, prior="uniform", name="input_dropout"),  # 0.0
                Integer(low=64, high=256, prior="uniform", name="num_trees", dtype=int),
            ]
            + self.trainer.SPACE,
            "TabNet": [
                Integer(low=4, high=16, prior="uniform", name="n_d", dtype=int),  # 8
                Integer(low=4, high=16, prior="uniform", name="n_a", dtype=int),  # 8
                Integer(low=1, high=6, prior="uniform", name="n_steps", dtype=int),  # 3
                Real(low=1.0, high=1.5, prior="uniform", name="gamma"),  # 1.3
                Integer(
                    low=1, high=4, prior="uniform", name="n_independent", dtype=int
                ),  # 2
                Integer(
                    low=1, high=4, prior="uniform", name="n_shared", dtype=int
                ),  # 2
            ]
            + self.trainer.SPACE,
            "TabTransformer": [
                Categorical(categories=[8, 16, 32], name="input_embed_dim"),
                Real(low=0, high=0.3, prior="uniform", name="embedding_dropout"),  # 0.1
                Real(low=0, high=0.3, prior="uniform", name="ff_dropout"),  # 0.1
                Categorical([2, 4, 8], name="num_heads"),  # 8
                Integer(
                    low=4,
                    high=8,
                    prior="uniform",
                    name="num_attn_blocks",
                    dtype=int,
                ),  # 6
                Real(low=0, high=0.3, prior="uniform", name="attn_dropout"),  # 0.1
                Real(low=0, high=0.3, prior="uniform", name="add_norm_dropout"),  # 0.1
                Integer(
                    low=2,
                    high=6,
                    prior="uniform",
                    name="ff_hidden_multiplier",
                    dtype=int,
                ),  # 4
            ]
            + self.trainer.SPACE,
            "AutoInt": [
                Real(low=0, high=0.3, prior="uniform", name="attn_dropouts"),  # 0.0
                # Categorical([16, 32, 64, 128], name='attn_embed_dim'),  # 32
                Real(low=0, high=0.3, prior="uniform", name="dropout"),  # 0.0
                Categorical([4, 8, 16, 32], name="embedding_dim"),  # 16
                Real(low=0, high=0.3, prior="uniform", name="embedding_dropout"),  # 0.0
                Integer(
                    low=1,
                    high=4,
                    prior="uniform",
                    name="num_attn_blocks",
                    dtype=int,
                ),  # 3
                Categorical([1, 2, 4], name="num_heads"),
            ]
            + self.trainer.SPACE,
            "FTTransformer": [
                Categorical(categories=[8, 16, 32], name="input_embed_dim"),
                Real(low=0, high=0.3, prior="uniform", name="embedding_dropout"),  # 0.1
                Categorical([2, 4, 8], name="num_heads"),
                Integer(
                    low=2,
                    high=4,
                    prior="uniform",
                    name="num_attn_blocks",
                    dtype=int,
                ),  # 6
                Real(low=0, high=0.3, prior="uniform", name="attn_dropout"),  # 0.1
                Real(low=0, high=0.3, prior="uniform", name="add_norm_dropout"),  # 0.1
                Real(low=0, high=0.3, prior="uniform", name="ff_dropout"),  # 0.1
                Integer(
                    low=2,
                    high=6,
                    prior="uniform",
                    name="ff_hidden_multiplier",
                    dtype=int,
                ),  # 4
            ]
            + self.trainer.SPACE,
            "GATE": [
                Integer(low=2, high=10, prior="uniform", name="gflu_stages", dtype=int),
                Real(low=0.0, high=0.3, prior="uniform", name="gflu_dropout"),
                Integer(low=2, high=4, prior="uniform", name="tree_depth", dtype=int),
                Integer(low=10, high=20, prior="uniform", name="num_trees", dtype=int),
                Real(low=0.0, high=0.3, prior="uniform", name="tree_dropout"),
                Real(
                    low=0.0,
                    high=0.3,
                    prior="uniform",
                    name="tree_wise_attention_dropout",
                ),
                Real(low=0.0, high=0.3, prior="uniform", name="embedding_dropout"),
            ]
            + self.trainer.SPACE,
        }
        return space_dict[model_name]

    def _initial_values(self, model_name):
        params_dict = {
            "Category Embedding": {
                "dropout": 0.0,
                "embedding_dropout": 0.1,
            },
            "NODE": {
                "depth": 4,
                "embedding_dropout": 0.0,
                "input_dropout": 0.0,
                "num_trees": 256,
            },
            "TabNet": {
                "n_d": 8,
                "n_a": 8,
                "n_steps": 3,
                "gamma": 1.3,
                "n_independent": 2,
                "n_shared": 2,
            },
            "TabTransformer": {
                "input_embed_dim": 32,
                "embedding_dropout": 0.1,
                "ff_dropout": 0.1,
                "num_heads": 8,
                "num_attn_blocks": 6,
                "attn_dropout": 0.1,
                "add_norm_dropout": 0.1,
                "ff_hidden_multiplier": 4,
            },
            "AutoInt": {
                "attn_dropouts": 0.0,
                "dropout": 0.0,
                "embedding_dim": 16,
                "embedding_dropout": 0.0,
                "num_attn_blocks": 3,
                "num_heads": 2,
            },
            "FTTransformer": {
                "input_embed_dim": 32,
                "embedding_dropout": 0.1,
                "num_heads": 8,
                "num_attn_blocks": 4,
                "attn_dropout": 0.1,
                "add_norm_dropout": 0.1,
                "ff_dropout": 0.1,
                "ff_hidden_multiplier": 4,
            },
            "GATE": {
                "gflu_stages": 6,
                "gflu_dropout": 0.0,
                # ``tree_depth`` influences the memory usage a lot. ``tree_depth``==10 with other default settings consumes
                # about 4 GiBs of ram.
                # When "tree_depth" larger than 4, and num_trees larger than 20 (approximately), performance on GPU
                # decreases dramatically.
                "tree_depth": 4,
                "num_trees": 20,
                "tree_dropout": 0.0,
                "tree_wise_attention_dropout": 0.0,
                "embedding_dropout": 0.1,
            },
        }
        for key in params_dict.keys():
            params_dict[key].update(self.trainer.chosen_params)
        return params_dict[model_name]


def pytorch_tabular_forward(self, backbone_features: torch.Tensor) -> Dict[str, Any]:
    setattr(self, "_hidden_representation", backbone_features)
    y_hat = self.head(backbone_features)
    y_hat = self.apply_output_sigmoid_scaling(y_hat)
    return self.pack_output(y_hat, backbone_features)


class PytorchTabularWrapper(AbstractWrapper):
    def __init__(self, model: PytorchTabular):
        super(PytorchTabularWrapper, self).__init__(model=model)
        if self.model_name == "TabNet":
            raise Exception(f"Wrapping TabNet is not supported.")

    def wrap_forward(self):
        from pytorch_tabular.models.base_model import BaseModel

        component = self.wrapped_model.model[self.model_name].model
        self.original_forward = component.compute_head
        component.compute_head = pytorch_tabular_forward.__get__(component, BaseModel)

    def reset_forward(self):
        if self.original_forward is not None:
            component = self.wrapped_model.model[self.model_name].model
            component.compute_head = self.original_forward

    @property
    def hidden_rep_dim(self):
        from pytorch_tabular.models.common.heads import LinearHead, MixtureDensityHead

        head = self.wrapped_model.model[self.model_name].model.head
        if type(head) == LinearHead:
            return head.layers[0].in_features
        elif type(head) == MixtureDensityHead:
            return head.pi.in_features
        else:
            raise Exception(
                f"Only LinearHead and MixtureDensityHead is supported to extract a hidden_rep_dim, but "
                f"got {type(head)} instead. It might be a customized one."
            )

    @property
    def hidden_representation(self):
        return getattr(
            self.wrapped_model.model[self.model_name].model, "_hidden_representation"
        )


class PytorchTabularVerboseLossCallback(Callback):
    def on_train_batch_end(
        self,
        trainer: "pl.Trainer",
        pl_module: pl.LightningModule,
        outputs,
        batch: Any,
        batch_idx: int,
    ) -> None:
        pl_module.log(
            "train_loss_verbose",
            outputs["loss"],
            on_step=False,
            on_epoch=True,
            batch_size=batch["target"].shape[0],
        )

    def on_validation_end(
        self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"
    ) -> None:
        trainer.callback_metrics["valid_loss_verbose"] = trainer.callback_metrics[
            "valid_loss"
        ]
