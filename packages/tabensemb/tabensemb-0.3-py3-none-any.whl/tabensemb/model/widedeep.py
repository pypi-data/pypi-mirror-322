from .base import AbstractWrapper
from torch import nn
from tabensemb.utils import *
from tabensemb.model import AbstractModel
from skopt.space import Integer, Categorical, Real
from packaging import version

if version.parse(torch.__version__) < version.parse("2.0.0"):
    # From pytorch_widedeep > 1.2.2, it imports LRScheduler instead of _LRScheduler
    from torch.optim.lr_scheduler import _LRScheduler

    torch.optim.lr_scheduler.LRScheduler = _LRScheduler


class WideDeep(AbstractModel):
    def __init__(self, *args, **kwargs):
        super(WideDeep, self).__init__(*args, **kwargs)
        if len(self.trainer.label_name) > 1:
            raise Exception(
                f"pytorch-widedeep does not support multi-target tasks. "
                f"See https://github.com/jrzaurin/pytorch-widedeep/issues/152"
            )

    def _get_program_name(self):
        return "WideDeep"

    def _space(self, model_name):
        """
        Spaces are selected around default parameters.
        """
        _space_dict = {
            "TabMlp": [
                Real(low=0.0, high=0.3, prior="uniform", name="cat_embed_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="mlp_dropout"),
            ]
            + self.trainer.SPACE,
            "TabResnet": [
                Real(low=0.0, high=0.3, prior="uniform", name="cat_embed_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="mlp_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="blocks_dropout"),
            ]
            + self.trainer.SPACE,
            "TabTransformer": [
                Real(low=0.0, high=0.3, prior="uniform", name="cat_embed_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="mlp_dropout"),
                Categorical(categories=[8, 16, 32], name="input_dim"),
                Categorical(categories=[2, 4, 8], name="n_heads"),
                Integer(low=4, high=8, prior="uniform", name="n_blocks", dtype=int),
                Real(low=0.0, high=0.3, prior="uniform", name="attn_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="ff_dropout"),
            ]
            + self.trainer.SPACE,
            "TabNet": [
                Real(low=0.0, high=0.3, prior="uniform", name="cat_embed_dropout"),
                Integer(low=1, high=6, prior="uniform", name="n_steps", dtype=int),
                Integer(low=4, high=16, prior="uniform", name="step_dim", dtype=int),
                Integer(low=4, high=16, prior="uniform", name="attn_dim", dtype=int),
                Real(low=0.0, high=0.3, prior="uniform", name="dropout"),
                Integer(
                    low=1,
                    high=4,
                    prior="uniform",
                    name="n_glu_step_dependent",
                    dtype=int,
                ),
                Integer(low=1, high=4, prior="uniform", name="n_glu_shared", dtype=int),
                Real(low=1.0, high=1.5, prior="uniform", name="gamma"),
            ]
            + self.trainer.SPACE,
            "SAINT": [
                Real(low=0.0, high=0.3, prior="uniform", name="cat_embed_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="mlp_dropout"),
                Categorical(categories=[4, 8, 16], name="input_dim"),
                Categorical(categories=[1, 2, 4], name="n_heads"),
                Integer(low=1, high=4, prior="uniform", name="n_blocks", dtype=int),
                Real(low=0.0, high=0.3, prior="uniform", name="attn_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="ff_dropout"),
            ]
            + self.trainer.SPACE,
            "ContextAttentionMLP": [
                Real(low=0.0, high=0.3, prior="uniform", name="cat_embed_dropout"),
                Categorical(categories=[8, 16, 32], name="input_dim"),
                Integer(low=2, high=4, prior="uniform", name="n_blocks", dtype=int),
                Real(low=0.0, high=0.3, prior="uniform", name="attn_dropout"),
            ]
            + self.trainer.SPACE,
            "SelfAttentionMLP": [
                Real(low=0.0, high=0.3, prior="uniform", name="cat_embed_dropout"),
                Categorical(categories=[8, 16, 32], name="input_dim"),
                Categorical(categories=[2, 4, 8], name="n_heads"),
                Integer(low=2, high=4, prior="uniform", name="n_blocks", dtype=int),
                Real(low=0.0, high=0.3, prior="uniform", name="attn_dropout"),
            ]
            + self.trainer.SPACE,
            "FTTransformer": [
                Real(low=0.0, high=0.3, prior="uniform", name="cat_embed_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="mlp_dropout"),
                Categorical(categories=[8, 16, 32], name="input_dim"),
                Categorical(categories=[2, 4, 8], name="n_heads"),
                Integer(low=2, high=4, prior="uniform", name="n_blocks", dtype=int),
                Real(low=0.0, high=0.3, prior="uniform", name="attn_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="ff_dropout"),
                Real(low=0.4, high=0.6, prior="uniform", name="kv_compression_factor"),
            ]
            + self.trainer.SPACE,
            "TabPerceiver": [
                Real(low=0.0, high=0.3, prior="uniform", name="cat_embed_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="mlp_dropout"),
                Categorical(categories=[8, 16, 32], name="input_dim"),
                Categorical(categories=[2, 4], name="n_cross_attn_heads"),
                Categorical(categories=[2, 4, 8], name="n_latents"),
                Categorical(categories=[16, 32, 64], name="latent_dim"),
                Categorical(categories=[2, 4], name="n_latent_heads"),
                Integer(
                    low=2, high=4, prior="uniform", name="n_latent_blocks", dtype=int
                ),
                Integer(
                    low=2, high=4, prior="uniform", name="n_perceiver_blocks", dtype=int
                ),
                Real(low=0.0, high=0.3, prior="uniform", name="attn_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="ff_dropout"),
            ]
            + self.trainer.SPACE,
            "TabFastFormer": [
                Real(low=0.0, high=0.3, prior="uniform", name="cat_embed_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="mlp_dropout"),
                Categorical(categories=[8, 16, 32], name="input_dim"),
                Categorical(categories=[2, 4, 8], name="n_heads"),
                Integer(low=2, high=4, prior="uniform", name="n_blocks", dtype=int),
                Real(low=0.0, high=0.3, prior="uniform", name="attn_dropout"),
                Real(low=0.0, high=0.3, prior="uniform", name="ff_dropout"),
            ]
            + self.trainer.SPACE,
        }
        return _space_dict[model_name]

    def _initial_values(self, model_name):
        _value_dict = {
            "TabMlp": {
                "cat_embed_dropout": 0.1,
                "mlp_dropout": 0.1,
            },
            "TabResnet": {
                "cat_embed_dropout": 0.1,
                "mlp_dropout": 0.1,
                "blocks_dropout": 0.1,
            },
            "TabTransformer": {
                "cat_embed_dropout": 0.1,
                "mlp_dropout": 0.1,
                "input_dim": 32,
                "n_heads": 8,
                "n_blocks": 6,
                "attn_dropout": 0.1,
                "ff_dropout": 0.1,
            },
            "TabNet": {
                "cat_embed_dropout": 0.1,
                "n_steps": 3,
                "step_dim": 8,
                "attn_dim": 8,
                "dropout": 0.0,
                "n_glu_step_dependent": 2,
                "n_glu_shared": 2,
                "gamma": 1.3,
            },
            "SAINT": {
                "cat_embed_dropout": 0.1,
                "mlp_dropout": 0.1,
                "input_dim": 16,
                "n_heads": 4,
                "n_blocks": 2,
                "attn_dropout": 0.2,
                "ff_dropout": 0.1,
            },
            "ContextAttentionMLP": {
                "cat_embed_dropout": 0.1,
                "input_dim": 32,
                "n_blocks": 3,
                "attn_dropout": 0.2,
            },
            "SelfAttentionMLP": {
                "cat_embed_dropout": 0.1,
                "input_dim": 32,
                "n_heads": 8,
                "n_blocks": 3,
                "attn_dropout": 0.2,
            },
            "FTTransformer": {
                "cat_embed_dropout": 0.1,
                "mlp_dropout": 0.1,
                "input_dim": 32,
                "n_heads": 8,
                "n_blocks": 4,
                "attn_dropout": 0.1,
                "ff_dropout": 0.1,
                "kv_compression_factor": 0.5,
            },
            "TabPerceiver": {
                "cat_embed_dropout": 0.1,
                "mlp_dropout": 0.1,
                "input_dim": 32,
                "n_cross_attn_heads": 4,
                "n_latents": 8,  # 16 by default in widedeep.
                "latent_dim": 64,  # 128 by default in widedeep.
                "n_latent_heads": 4,
                "n_latent_blocks": 4,
                "n_perceiver_blocks": 4,
                "attn_dropout": 0.2,
                "ff_dropout": 0.1,
            },
            "TabFastFormer": {
                "cat_embed_dropout": 0.1,
                "mlp_dropout": 0.1,
                "input_dim": 32,
                "n_heads": 8,
                "n_blocks": 4,
                "attn_dropout": 0.2,
                "ff_dropout": 0.1,
            },
        }
        for key in _value_dict.keys():
            _value_dict[key].update(self.trainer.chosen_params)
        return _value_dict[model_name]

    def _new_model(self, model_name, verbose, **kwargs):
        from pytorch_widedeep.models import (
            WideDeep,
            TabMlp,
            TabResnet,
            TabTransformer,
            TabNet,
            SAINT,
            ContextAttentionMLP,
            SelfAttentionMLP,
            FTTransformer,
            TabPerceiver,
            TabFastFormer,
        )
        from pytorch_widedeep import Trainer as wd_Trainer

        cont_feature_names = self.trainer.cont_feature_names
        cat_feature_names = self.trainer.cat_feature_names

        (
            opt_name,
            opt_params,
            lrs_name,
            lrs_params,
        ) = self._update_optimizer_lr_scheduler_params(model_name=model_name, **kwargs)
        model_args = {
            key: value
            for key, value in kwargs.items()
            if key not in ["lr", "batch_size", "original_batch_size"]
            and key not in opt_params.keys()
            and key not in lrs_params.keys()
        }
        args = dict(
            column_idx=self.tab_preprocessor.column_idx,
            continuous_cols=cont_feature_names,
            cat_embed_input=(
                self.tab_preprocessor.cat_embed_input
                if len(cat_feature_names) != 0
                else None
            ),
            **model_args,
        )

        if model_name == "TabTransformer":
            args["embed_continuous"] = True if len(cat_feature_names) == 0 else False

        mapping = {
            "TabMlp": TabMlp,
            "TabResnet": TabResnet,
            "TabTransformer": TabTransformer,
            "TabNet": TabNet,
            "SAINT": SAINT,
            "ContextAttentionMLP": ContextAttentionMLP,
            "SelfAttentionMLP": SelfAttentionMLP,
            "FTTransformer": FTTransformer,
            "TabPerceiver": TabPerceiver,
            "TabFastFormer": TabFastFormer,
        }

        task = self.trainer.datamodule.task
        loss = self.trainer.datamodule.loss
        if task == "binary" and loss == "cross_entropy":
            loss = "binary_cross_entropy"
        self.task = task

        tab_model = mapping[model_name](**args)
        if task == "multiclass":
            model = WideDeep(
                deeptabular=tab_model, pred_dim=self.trainer.datamodule.n_classes[0]
            )
        else:
            model = WideDeep(deeptabular=tab_model)

        optimizer = getattr(torch.optim, opt_name)(model.parameters(), **opt_params)
        lr_scheduler = getattr(torch.optim.lr_scheduler, lrs_name)(
            optimizer, **lrs_params
        )

        wd_trainer = wd_Trainer(
            model,
            objective=loss,
            verbose=0,
            device="cpu" if self.trainer.device == "cpu" else "cuda",
            num_workers=0,
            optimizers=optimizer,
            lr_schedulers=lr_scheduler,
        )
        return wd_trainer

    def _train_data_preprocess(self, model_name, warm_start=False):
        import pytorch_widedeep
        from pytorch_widedeep.preprocessing import TabPreprocessor
        from pandas._config import option_context

        data = self.trainer.datamodule
        cont_feature_names = self.trainer.cont_feature_names
        cat_feature_names = self.trainer.cat_feature_names
        if not warm_start:
            if version.parse(pytorch_widedeep.__version__) < version.parse("1.2.3"):
                tab_preprocessor = TabPreprocessor(
                    continuous_cols=cont_feature_names,
                    cat_embed_cols=(
                        cat_feature_names if len(cat_feature_names) != 0 else None
                    ),
                )
            else:
                # https://github.com/jrzaurin/pytorch-widedeep/commit/cc0d1ad59c447dabd29072a552194ece12173778#diff-2f6e79eedee796c7edeac4fffc29ef35ecbfb8c234ff63313509e412a8d3ed42L108
                tab_preprocessor = TabPreprocessor(
                    continuous_cols=cont_feature_names,
                    cat_embed_cols=(
                        cat_feature_names if len(cat_feature_names) != 0 else None
                    ),
                    cols_to_scale=cont_feature_names,
                )
            with option_context("mode.chained_assignment", None):
                X_tab_train = tab_preprocessor.fit_transform(data.X_train)
                X_tab_val = tab_preprocessor.transform(data.X_val)
                X_tab_test = tab_preprocessor.transform(data.X_test)
            self.tab_preprocessor = tab_preprocessor
        else:
            with option_context("mode.chained_assignment", None):
                X_tab_train = self.tab_preprocessor.transform(data.X_train)
                X_tab_val = self.tab_preprocessor.transform(data.X_val)
                X_tab_test = self.tab_preprocessor.transform(data.X_test)
        return {
            "X_train": X_tab_train,
            "y_train": data.y_train.flatten(),
            "X_val": X_tab_val,
            "y_val": data.y_val.flatten(),
            "X_test": X_tab_test,
            "y_test": data.y_test.flatten(),
        }

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
        """
        pytorch_widedeep uses an approximated loss calculation procedure that calculates the average loss
        across batches, which is not what we do (in a precise way for MSE) at the end of training and makes
        results from the callback differ from our final metrics.
        """
        from ._widedeep.widedeep_callback import WideDeepCallback, EarlyStopping

        es_callback = EarlyStopping(
            patience=self.trainer.static_params["patience"],
            verbose=1 if verbose else 0,
            restore_best_weights=True,
        )

        model._set_callbacks_and_metrics(
            callbacks=[
                es_callback,
                WideDeepCallback(total_epoch=epoch, verbose=verbose),
            ],
            metrics=None,
        )
        if warm_start:
            # The model is stored in cpu after loaded from disk. And widedeep does not make model and data on the
            # same device. Also note that when _finetune and cuda is available, data.cuda() is called.
            from pytorch_widedeep.training import _finetune

            _finetune.use_cuda = self.device == "cuda"
        model.fit(
            X_train={"X_tab": X_train, "target": y_train},
            X_val={"X_tab": X_val, "target": y_val},
            n_epochs=epoch if not warm_start else 1,
            batch_size=int(kwargs["batch_size"]),
            finetune=warm_start,
            finetune_epochs=10,
        )

        self.train_losses[model_name] = model.history["train_loss"]
        self.val_losses[model_name] = model.history["val_loss"]
        self.restored_epochs[model_name] = es_callback.best_epoch

    def _pred_single_model(self, model, X_test, verbose, **kwargs):
        original_batch_size = model.batch_size
        delattr(model, "batch_size")
        if self.task == "regression":
            res = model.predict(X_tab=X_test, batch_size=len(X_test)).reshape(-1, 1)
        elif self.task == "binary":
            res = model.predict_proba(X_tab=X_test, batch_size=len(X_test))[
                :, 1
            ].reshape(-1, 1)
        else:
            res = model.predict_proba(X_tab=X_test, batch_size=len(X_test))
        setattr(model, "batch_size", original_batch_size)
        return res

    def _data_preprocess(self, df, derived_data, model_name):
        # SettingWithCopyWarning in TabPreprocessor.transform
        # i.e. df_cont[self.standardize_cols] = self.scaler.transform(df_std.values)
        from pandas._config import option_context

        with option_context("mode.chained_assignment", None):
            X_df = self.tab_preprocessor.transform(df)
        return X_df

    @staticmethod
    def _get_model_names():
        return [
            "TabMlp",
            "TabResnet",
            "TabTransformer",
            "TabNet",
            "SAINT",
            "ContextAttentionMLP",
            "SelfAttentionMLP",
            "FTTransformer",
            "TabPerceiver",
            "TabFastFormer",
        ]


def widedeep_forward(self, input):
    """
    This is the forward of nn.Sequential because WideDeep model is a nn.Module and WideDeep.deeptabular is a
    nn.Sequential where the last module is a linear layer.
    """
    l = len(self)
    for idx, module in enumerate(self):
        if idx == l - 1:
            setattr(self, "_hidden_representation", input)
        input = module(input)
    return input


class WideDeepWrapper(AbstractWrapper):
    def __init__(self, model: WideDeep):
        super(WideDeepWrapper, self).__init__(model=model)
        if self.model_name == "TabNet":
            raise Exception(f"Wrapping TabNet is not supported.")

    def wrap_forward(self):
        component = self.wrapped_model.model[self.model_name].model.deeptabular
        self.original_forward = component.forward
        component.forward = widedeep_forward.__get__(component, nn.Sequential)

    def reset_forward(self):
        component = self.wrapped_model.model[self.model_name].model.deeptabular
        component.forward = self.original_forward

    @property
    def hidden_rep_dim(self):
        """
        In pytorch_widedeep.models.wide_deep, see WideDeep_add_pred_layer()
        """
        component = self.wrapped_model.model[self.model_name].model
        if component.deeptext is not None or component.deepimage is not None:
            warnings.warn(
                f"The WideDeep model has deeptext or deepimage component, which is not supported for "
                f"hidden representation extraction."
            )
        return component.deeptabular[0].output_dim

    @property
    def hidden_representation(self):
        component = self.wrapped_model.model[self.model_name].model.deeptabular
        return getattr(component, "_hidden_representation")
