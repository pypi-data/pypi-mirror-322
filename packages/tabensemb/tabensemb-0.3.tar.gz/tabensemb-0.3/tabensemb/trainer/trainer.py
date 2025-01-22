import os.path
import warnings
import matplotlib.figure
import matplotlib.axes
import matplotlib.legend
import numpy as np
import pandas as pd
import tabensemb
from tabensemb.utils import *
from tabensemb.config import UserConfig
from tabensemb.data import DataModule
from tabensemb.data.utils import get_imputed_dtype, fill_cat_nan
from copy import deepcopy as cp
from skopt.space import Real, Integer, Categorical
import time
from typing import *
import torch.nn as nn
import torch.cuda
import torch.utils.data as Data
import scipy.stats as st
from sklearn.utils import resample as skresample
import platform, psutil, subprocess
import shutil
import pickle

set_random_seed(tabensemb.setting["random_seed"])


class Trainer:
    """
    The model manager that provides saving, loading, ranking, and analyzing utilities.

    Attributes
    ----------
    args
        A :class:`tabensemb.config.UserConfig` instance.
    configfile
        The source of the configuration. If the ``config`` argument of :meth:`load_config` is a
        :class:`tabensemb.config.UserConfig`, it is "UserInputConfig". If the ``config`` argument is a path, it is the
        path. If the ``config`` argument is not given, it is the "base" argument passed to python when executing the
        script.
    datamodule
        A :class:`tabensemb.data.datamodule.DataModule` instance.
    device
        The device on which models are trained. "cpu", "cuda", or "cuda:X".
    leaderboard
        The ranking of all models in all model bases. Only valid after :meth:`get_leaderboard` is called.
    modelbases
        A list of :class:`tabensemb.model.AbstractModel`.
    modelbases_names
        Corresponding names (:attr:`tabensemb.model.AbstractModel.program`) of :attr:`modelbases`.
    project
        The name of the :class:`Trainer`.
    project_root
        The place where all files are stored.
        ``tabensemb.setting["default_output_path"]`` ``/{project}/{project_root_subfolder}/{TIME}-{config}`` where ``project`` is :attr:`project`,
        ``project_root_subfolder`` and ``config`` are arguments of :meth:`load_config`.
    sys_summary
        Summary of the system when :meth:`summarize_device` is called.
    SPACE
    all_feature_names
    cat_feature_mapping
    cat_feature_names
    chosen_params
    cont_feature_names
    derived_data
    derived_stacked_features
    df
    feature_data
    label_data
    label_name
    static_params
    tensors
    test_indices
    train_indices
    training
    unscaled_feature_data
    unscaled_label_data
    val_indices
    """

    def __init__(self, device: str = "cpu", project: str = None):
        """
        The bridge of all modules. It contains all configurations and data. It can train model bases and evaluate
        results (including feature importance, partial dependency, etc.).

        Parameters
        ----------
        device:
            The device on which models are trained. Choose from "cpu", "cuda", or "cuda:X" (if available).
        project:
            The name of the :class:`Trainer`.
        """
        self.device = "cpu"
        self.project = project
        self.modelbases = []
        self.modelbases_names = []
        self.set_device(device)

    def set_device(self, device: str):
        """
        Set the device on which models are trained.

        Parameters
        ----------
        device
            "cpu", "cuda", or "cuda:X" (if available)

        Notes
        -----
        Multi-GPU training and training on a machine with multiple GPUs are not tested.
        """
        if device not in ["cpu", "cuda"] and "cuda" not in device:
            raise Exception(
                f"Device {device} is an invalid selection. Choose among {['cpu', 'cuda']}."
                f"Note: Multi-GPU training and training on a machine with multiple GPUs are not tested."
            )
        self.device = device

    def add_modelbases(self, models: List):
        """
        Add a list of model bases and check whether their names conflict.

        Parameters
        ----------
        models:
            A list of :class:`tabensemb.model.AbstractModel`.
        """
        new_modelbases_names = self.modelbases_names + [x.program for x in models]
        if len(new_modelbases_names) != len(list(set(new_modelbases_names))):
            raise Exception(f"Conflicted model base names: {self.modelbases_names}")
        self.modelbases += models
        self.modelbases_names = new_modelbases_names

    def get_modelbase(self, program: str):
        """
        Get the selected model base by its name.

        Parameters
        ----------
        program
            The name of the model base.

        Returns
        -------
        AbstractModel
            A model base.
        """
        if program not in self.modelbases_names:
            raise Exception(f"Model base {program} not added to the trainer.")
        return self.modelbases[self.modelbases_names.index(program)]

    def clear_modelbase(self):
        """
        Delete all model bases in the :class:`Trainer`.
        """
        self.modelbases = []
        self.modelbases_names = []

    def detach_modelbase(self, program: str, verbose: bool = True) -> "Trainer":
        """
        Detach the selected model base to a separate :class:`Trainer` and save it to another directory. It is much cheaper than
        :meth:`copy` if only one model base is needed. If any external model is required, please use :meth:``detach_model``
        to detach a single model.

        Parameters
        ----------
        program
            The selected model base.
        verbose
            Verbosity

        Returns
        -------
        Trainer
            A :class:`Trainer` with the selected model base.

        See Also
        --------
        :meth:`copy`, :meth:`detach_model`, :meth:`tabensemb.model.AbstractModel.detach_model`
        """
        modelbase = cp(self.get_modelbase(program=program))
        tmp_trainer = modelbase.trainer
        tmp_trainer.clear_modelbase()
        new_path = safe_mkdir(add_postfix(self.project_root))
        tmp_trainer.set_path(new_path, verbose=False)
        modelbase.set_path(os.path.join(new_path, modelbase.program))
        tmp_trainer.add_modelbases([modelbase])
        shutil.copytree(self.get_modelbase(program=program).root, modelbase.root)
        save_trainer(tmp_trainer, verbose=verbose)
        return tmp_trainer

    def detach_model(
        self, program: str, model_name: str, verbose: bool = True
    ) -> "Trainer":
        """
        Detach the selected model of the selected model base to a separate :class:`Trainer` and save it to another
        directory. If external models are required, they are also detached into the separated Trainer.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model.
        verbose
            Verbosity.

        Returns
        -------
        Trainer
            A :class:`Trainer` with the selected model in its model base.
        """
        required_models_names = self.get_modelbase(program=program).required_models(
            model_name
        )
        if required_models_names is not None and any(
            [x.startswith("EXTERN") for x in required_models_names]
        ):
            tmp_trainer = self.copy()
            tmp_modelbase = tmp_trainer.get_modelbase(program=program)
            detached_model = tmp_modelbase.detach_model(
                model_name=model_name, program=f"{program}_{model_name}"
            )
            required_models = tmp_modelbase._get_required_models(model_name)
            required_modelbases = (
                [
                    model
                    for x, model in required_models.items()
                    if x.startswith("EXTERN")
                ]
                if required_models is not None
                else []
            )
        else:
            tmp_trainer = self.detach_modelbase(program=program, verbose=False)
            tmp_modelbase = tmp_trainer.get_modelbase(program=program)
            detached_model = tmp_modelbase.detach_model(
                model_name=model_name, program=f"{program}_{model_name}"
            )
            required_modelbases = []
        tmp_trainer.clear_modelbase()
        tmp_trainer.add_modelbases([detached_model] + required_modelbases)
        shutil.rmtree(tmp_modelbase.root)
        save_trainer(tmp_trainer, verbose=verbose)
        return tmp_trainer

    def copy(self) -> "Trainer":
        """
        Copy the :class:`Trainer` and save it to another directory. It might be time and space-consuming because all
        model bases are copied once.

        Returns
        -------
        trainer
            A :class:`Trainer` instance.

        See Also
        --------
        :meth:`detach_modelbase`, :meth:`detach_model`, :meth:`tabensemb.model.AbstractModel.detach_model`
        """
        tmp_trainer = cp(self)
        new_path = safe_mkdir(add_postfix(self.project_root))
        tmp_trainer.set_path(new_path, verbose=True)
        for modelbase in tmp_trainer.modelbases:
            modelbase.set_path(os.path.join(new_path, modelbase.program))
        shutil.copytree(self.project_root, tmp_trainer.project_root, dirs_exist_ok=True)
        save_trainer(tmp_trainer)
        return tmp_trainer

    def load_config(
        self,
        config: Union[str, UserConfig] = None,
        manual_config: Dict = None,
        project_root_subfolder: str = None,
    ) -> None:
        """
        Load the configuration using a :class:`tabensemb.config.UserConfig` or a file in .py or .json format.
        Arguments passed to python when executing the script are parsed using ``argparse`` if ``config`` is
        left None. All keys in :meth:`tabensemb.config.UserConfig.defaults` can be parsed, for example:
        For the loss function: ``--loss mse``,
        For the total epoch: ``--epoch 200``,
        For the option of bayes opt: ``--bayes_opt`` to turn on Bayesian hyperparameter optimization,
        ``--no-bayes_opt`` to turn it off.
        The loaded configuration will be saved as a .py file in the project folder.

        Parameters
        ----------
        config
            It can be the path to the configuration file in json or python format, or a
            :class:`tabensemb.config.UserConfig` instance. If it is None, arguments passed to python will be parsed.
            If it is a path, it will be passed to :meth:`tabensemb.config.UserConfig.from_file`.
        manual_config
            Update the configuration with a dict. For example: ``manual_config={"bayes_opt": True}``.
        project_root_subfolder
            The subfolder that the project will be locate in. The folder name will be
            ``tabensemb.setting["default_output_path"]`` ``/{project}/{project_root_subfolder}/{TIME}-{config}``
        """
        input_config = config is not None
        if isinstance(config, str) or not input_config:
            # The base config is loaded using the --base argument
            if is_notebook() and not input_config:
                raise Exception(
                    "A config file must be assigned in notebook environment."
                )
            elif is_notebook() or input_config:
                parse_res = {"base": config}
            else:  # not notebook and config is None
                parse_res = UserConfig.parse()
            self.configfile = parse_res["base"]
            config = UserConfig(path=self.configfile)
            # Then, several args can be modified using other arguments like --lr, --weight_decay
            # only when a config file is not given so that configs depend on input arguments.
            if not is_notebook() and not input_config:
                # If the argument is not given in the command, the item will be None and will not be merged into
                # `config` using the `merge` method.
                config.merge(parse_res)
            if manual_config is not None:
                config.merge(manual_config)
            self.args = config
        else:
            self.configfile = "UserInputConfig"
            if manual_config is not None:
                warnings.warn(f"manual_config is ignored when config is an UserConfig.")
            self.args = config

        self.datamodule = DataModule(self.args)

        self.project = self.args["database"] if self.project is None else self.project
        self._create_dir(project_root_subfolder=project_root_subfolder)
        config.to_file(os.path.join(self.project_root, "args.py"))

    @property
    def static_params(self) -> Dict:
        """
        The "patience" and "epoch" parameters in the configuration.
        """
        return {
            "patience": self.args["patience"],
            "epoch": self.args["epoch"],
        }

    @property
    def chosen_params(self):
        """
        The "lr", "weight_decay", and "batch_size" parameters in the configuration.
        """
        return {
            "lr": self.args["lr"],
            "weight_decay": self.args["weight_decay"],
            "batch_size": self.args["batch_size"],
        }

    @property
    def SPACE(self):
        """
        Search spaces for "lr", "weight_decay", and "batch_size" defined in the configuration.
        """
        SPACE = []
        for var in self.args["SPACEs"].keys():
            setting = cp(self.args["SPACEs"][var])
            ty = setting["type"]
            setting.pop("type")
            if ty == "Real":
                SPACE.append(Real(name=var, **setting))
            elif ty == "Categorical":
                SPACE.append(Categorical(name=var, **setting))
            elif ty == "Integer":
                SPACE.append(Integer(name=var, **setting))
            else:
                raise Exception("Invalid type of skopt space.")
        return SPACE

    @property
    def feature_data(self) -> pd.DataFrame:
        """
        :meth:`tabensemb.data.datamodule.DataModule.feature_data`
        """
        return self.datamodule.feature_data if hasattr(self, "datamodule") else None

    @property
    def unscaled_feature_data(self):
        """
        :meth:`tabensemb.data.datamodule.DataModule.unscaled_feature_data`
        """
        return (
            self.datamodule.unscaled_feature_data
            if hasattr(self, "datamodule")
            else None
        )

    @property
    def unscaled_label_data(self):
        """
        :meth:`tabensemb.data.datamodule.DataModule.unscaled_label_data`
        """
        return (
            self.datamodule.unscaled_label_data if hasattr(self, "datamodule") else None
        )

    @property
    def label_data(self) -> pd.DataFrame:
        """
        :meth:`tabensemb.data.datamodule.DataModule.label_data`
        """
        return self.datamodule.label_data if hasattr(self, "datamodule") else None

    @property
    def derived_data(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.derived_data`
        """
        return self.datamodule.derived_data if hasattr(self, "datamodule") else None

    @property
    def cont_feature_names(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.cont_feature_names`
        """
        return (
            self.datamodule.cont_feature_names if hasattr(self, "datamodule") else None
        )

    @property
    def cat_feature_names(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.cat_feature_names`
        """
        return (
            self.datamodule.cat_feature_names if hasattr(self, "datamodule") else None
        )

    @property
    def all_feature_names(self):
        """
        :meth:`tabensemb.data.datamodule.DataModule.all_feature_names`
        """
        return (
            self.datamodule.all_feature_names if hasattr(self, "datamodule") else None
        )

    @property
    def label_name(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.label_name`
        """
        return self.datamodule.label_name if hasattr(self, "datamodule") else None

    @property
    def train_indices(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.train_indices`
        """
        return self.datamodule.train_indices if hasattr(self, "datamodule") else None

    @property
    def val_indices(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.val_indices`
        """
        return self.datamodule.val_indices if hasattr(self, "datamodule") else None

    @property
    def test_indices(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.test_indices`
        """
        return self.datamodule.test_indices if hasattr(self, "datamodule") else None

    @property
    def df(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.df`
        """
        return self.datamodule.df if hasattr(self, "datamodule") else None

    @property
    def tensors(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.tensors`
        """
        return self.datamodule.tensors if hasattr(self, "datamodule") else None

    @property
    def cat_feature_mapping(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.cat_feature_mapping`
        """
        return (
            self.datamodule.cat_feature_mapping if hasattr(self, "datamodule") else None
        )

    @property
    def derived_stacked_features(self):
        """
        :meth:`tabensemb.data.datamodule.DataModule.derived_stacked_features`
        """
        return (
            self.datamodule.derived_stacked_features
            if hasattr(self, "datamodule")
            else None
        )

    @property
    def training(self):
        """
        :attr:`tabensemb.data.datamodule.DataModule.training`
        """
        return self.datamodule.training if hasattr(self, "datamodule") else None

    def set_status(self, training: bool):
        """
        A wrapper of :meth:`tabensemb.data.datamodule.DataModule.set_status`
        """
        self.datamodule.set_status(training)

    def load_data(self, *args, **kwargs):
        """
        A wrapper of :meth:`tabensemb.data.datamodule.DataModule.load_data`. The ``save_path`` argument is set to
        :attr:`project_root`.
        """
        if "save_path" in kwargs.keys():
            kwargs.__delitem__("save_path")
        self.datamodule.load_data(save_path=self.project_root, *args, **kwargs)

    def set_path(self, path: Union[os.PathLike, str], verbose=False):
        """
        Set the work directory of the :class:`Trainer`.

        Parameters
        ----------
        path
            The work directory.
        """
        self.project_root = path
        if not os.path.exists(self.project_root):
            os.mkdir(self.project_root)
        if verbose:
            print(f"The project will be saved to {self.project_root}")

    def _create_dir(self, verbose: bool = True, project_root_subfolder: str = None):
        """
        Create the folder for the :class:`Trainer`.

        Parameters
        ----------
        verbose
            Whether to print the path of the :class:`Trainer`.
        project_root_subfolder
            See :meth:`load_config`.
        """
        default_path = tabensemb.setting["default_output_path"]
        if not os.path.exists(default_path):
            os.makedirs(default_path, exist_ok=True)
        if project_root_subfolder is not None:
            if not os.path.exists(os.path.join(default_path, project_root_subfolder)):
                os.makedirs(
                    os.path.join(default_path, project_root_subfolder), exist_ok=True
                )
        subfolder = (
            self.project
            if project_root_subfolder is None
            else os.path.join(project_root_subfolder, self.project)
        )
        t = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        folder_name = t + "-0" + "_" + os.path.split(self.configfile)[-1]
        if not os.path.exists(os.path.join(default_path, subfolder)):
            os.makedirs(os.path.join(default_path, subfolder), exist_ok=True)
        self.set_path(
            safe_mkdir(os.path.join(default_path, subfolder, folder_name)),
            verbose=verbose,
        )

    def summarize_setting(self):
        """
        Print the summary of the device, the configuration, and the global setting of the package
        (``tabensemb.setting``).
        """
        print("Device:")
        print(pretty(self.summarize_device()))
        print("Configurations:")
        print(pretty(self.args))
        print(f"Global settings:")
        print(pretty(tabensemb.setting))

    def summarize_device(self):
        """
        Print a summary of the environment.
        https://www.thepythoncode.com/article/get-hardware-system-information-python
        """

        def get_size(bytes, suffix="B"):
            """
            Scale bytes to its proper format
            e.g:
                1253656 => '1.20MB'
                1253656678 => '1.17GB'
            """
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor

        def get_processor_info():
            if platform.system() == "Windows":
                return platform.processor()
            elif platform.system() == "Darwin":
                return (
                    subprocess.check_output(
                        ["/usr/sbin/sysctl", "-n", "machdep.cpu.brand_string"]
                    )
                    .strip()
                    .decode("utf-8")
                )
            elif platform.system() == "Linux":
                command = "cat /proc/cpuinfo"
                all_info = (
                    subprocess.check_output(command, shell=True).strip().decode("utf-8")
                )

                for string in all_info.split("\n"):
                    if "model name\t: " in string:
                        return string.split("\t: ")[1]
            return ""

        uname = platform.uname()
        cpufreq = psutil.cpu_freq()
        svmem = psutil.virtual_memory()
        self.sys_summary = {
            "System": uname.system,
            "Node name": uname.node,
            "System release": uname.release,
            "System version": uname.version,
            "Machine architecture": uname.machine,
            "Processor architecture": uname.processor,
            "Processor model": get_processor_info(),
            "Physical cores": psutil.cpu_count(logical=False),
            "Total cores": psutil.cpu_count(logical=True),
            "Max core frequency": f"{cpufreq.max:.2f}Mhz",
            "Total memory": get_size(svmem.total),
            "Python version": platform.python_version(),
            "Python implementation": platform.python_implementation(),
            "Python compiler": platform.python_compiler(),
            "Cuda availability": torch.cuda.is_available(),
            "GPU devices": [
                torch.cuda.get_device_properties(i).name
                for i in range(torch.cuda.device_count())
            ],
        }
        return self.sys_summary

    def train(
        self,
        programs: List[str] = None,
        verbose: bool = True,
        *args,
        **kwargs,
    ):
        """
        Train all model bases (:attr:`modelbases`).

        Parameters
        ----------
        programs
            A selected subset of model bases.
        verbose
            Verbosity.
        *args
            Arguments passed to :meth:`tabensemb.model.AbstractModel.train`
        **kwargs
            Arguments passed to :meth:`tabensemb.model.AbstractModel.train`
        """
        if programs is None:
            modelbases_to_train = self.modelbases
        else:
            modelbases_to_train = [self.get_modelbase(x) for x in programs]

        if len(modelbases_to_train) == 0:
            warnings.warn(
                f"No modelbase is trained. Please confirm that trainer.add_modelbases is called."
            )

        for modelbase in modelbases_to_train:
            modelbase.train(*args, verbose=verbose, **kwargs)

    def cross_validation(
        self,
        programs: List[str],
        n_random: int,
        verbose: bool,
        test_data_only: bool,
        split_type: str = "cv",
        load_from_previous: bool = False,
        **kwargs,
    ) -> Dict[str, Dict[str, Dict[str, Tuple[np.ndarray, np.ndarray]]]]:
        """
        Repeat :meth:`load_data`, train model bases, and evaluate all models for multiple times.

        Parameters
        ----------
        programs
            A selected subset of model bases.
        n_random
            The number of repeats.
        verbose
            Verbosity.
        test_data_only
            Whether to evaluate models only on testing datasets.
        split_type
            The type of data splitting. "random" and "cv" are supported. Ignored when ``load_from_previous`` is True.
        load_from_previous
            Load the state of a previous run (mostly because of an unexpected interruption).
        **kwargs
            Arguments for :meth:`tabensemb.model.AbstractModel.train`

        Notes
        -----
        The results of a continuous run and a continued run (``load_from_previous=True``) are consistent.

        Returns
        -------
        dict
            A dict in the following format:
            {keys: programs, values: {keys: model names, values: {keys: ["Training", "Testing", "Validation"], values:
            (Predicted values, true values)}}
        """
        programs_predictions = {}
        for program in programs:
            programs_predictions[program] = {}

        if load_from_previous:
            if not os.path.exists(
                os.path.join(self.project_root, "cv")
            ) or not os.path.isfile(
                os.path.join(self.project_root, "cv", "cv_state.pkl")
            ):
                raise Exception(f"No previous state to load from.")
            with open(
                os.path.join(self.project_root, "cv", "cv_state.pkl"), "rb"
            ) as file:
                current_state = pickle.load(file)
            start_i = current_state["i_random"]
            self.load_state(current_state["trainer"])
            programs_predictions = current_state["programs_predictions"]
            reloaded_once_predictions = current_state["once_predictions"]
            skip_program = reloaded_once_predictions is not None
            if start_i >= n_random:
                raise Exception(
                    f"The loaded state is incompatible with the current setting."
                )
            print(f"Previous cross validation state is loaded.")
            split_type = (
                "cv"
                if self.datamodule.datasplitter.cv_generator is not None
                else "random"
            )
        else:
            start_i = 0
            skip_program = False
            reloaded_once_predictions = None
            if split_type == "cv" and not self.datamodule.datasplitter.support_cv:
                warnings.warn(
                    f"{self.datamodule.datasplitter.__class__.__name__} does not support cross validation splitting. "
                    f"Use its original regime instead."
                )
                split_type = "random"
            self.datamodule.datasplitter.reset_cv(
                cv=n_random if split_type == "cv" else -1
            )
            if n_random > 0 and not os.path.exists(
                os.path.join(self.project_root, "cv")
            ):
                os.mkdir(os.path.join(self.project_root, "cv"))

        def func_save_state(state):
            with open(
                os.path.join(self.project_root, "cv", "cv_state.pkl"), "wb"
            ) as file:
                pickle.dump(state, file)

        for i in range(start_i, n_random):
            if verbose:
                print(
                    f"----------------------------{i + 1}/{n_random} {split_type}----------------------------"
                )
            trainer_state = cp(self)
            if not skip_program:
                current_state = {
                    "trainer": trainer_state,
                    "i_random": i,
                    "programs_predictions": programs_predictions,
                    "once_predictions": None,
                }
                func_save_state(current_state)
            with HiddenPrints(disable_std=not verbose):
                set_random_seed(tabensemb.setting["random_seed"] + i)
                self.load_data()
            once_predictions = {} if not skip_program else reloaded_once_predictions
            for program in programs:
                if skip_program:
                    if program in once_predictions.keys():
                        print(f"Skipping finished model base {program}")
                        continue
                    else:
                        skip_program = False
                modelbase = self.get_modelbase(program)
                modelbase.train(dump_trainer=True, verbose=verbose, **kwargs)
                predictions = modelbase._predict_all(
                    verbose=verbose, test_data_only=test_data_only
                )
                once_predictions[program] = predictions
                for model_name, value in predictions.items():
                    if model_name in programs_predictions[program].keys():
                        # current_predictions is a reference, so modifications are directly applied to it.
                        current_predictions = programs_predictions[program][model_name]

                        def append_once(key):
                            current_predictions[key] = (
                                np.append(
                                    current_predictions[key][0], value[key][0], axis=0
                                ),
                                np.append(
                                    current_predictions[key][1], value[key][1], axis=0
                                ),
                            )

                        append_once("Testing")
                        if not test_data_only:
                            append_once("Training")
                            append_once("Validation")
                    else:
                        programs_predictions[program][model_name] = value
                # It is expected that only model bases in self is changed. datamodule is not updated because the cross
                # validation status should remain before load_data() is called.
                trainer_state.modelbases = self.modelbases
                current_state = {
                    "trainer": trainer_state,
                    "i_random": i,
                    "programs_predictions": programs_predictions,
                    "once_predictions": once_predictions,
                }
                func_save_state(current_state)
            df_once = self._cal_leaderboard(
                once_predictions, test_data_only=test_data_only, save=False
            )
            df_once.to_csv(
                os.path.join(self.project_root, "cv", f"leaderboard_cv_{i}.csv")
            )
            trainer_state.modelbases = self.modelbases
            current_state = {
                "trainer": trainer_state,
                "i_random": i + 1,
                "programs_predictions": programs_predictions,
                "once_predictions": None,
            }
            func_save_state(current_state)
            if verbose:
                print(
                    f"--------------------------End {i + 1}/{n_random} {split_type}--------------------------"
                )
        return programs_predictions

    def get_leaderboard(
        self,
        test_data_only: bool = False,
        dump_trainer: bool = True,
        cross_validation: int = 0,
        verbose: bool = True,
        load_from_previous: bool = False,
        split_type: str = "cv",
        **kwargs,
    ) -> pd.DataFrame:
        """
        Run all model bases with/without cross validation for a leaderboard.

        Parameters
        ----------
        test_data_only
            Whether to evaluate models only on testing datasets.
        dump_trainer
            Whether to save the :class:`Trainer`.
        cross_validation
            The number of cross-validation. See :meth:`cross_validation`. 0 to evaluate current trained models on the
            current dataset.
        verbose
            Verbosity.
        load_from_previous
            Load the state of a previous run (mostly because of an unexpected interruption).
        split_type
            The type of data splitting. "random" and "cv" are supported. Ignored when ``load_from_previous`` is True.
        **kwargs
            Arguments for :meth:`tabensemb.model.AbstractModel.train`

        Returns
        -------
        pd.DataFrame
            The leaderboard.
        """
        if len(self.modelbases) == 0:
            raise Exception(
                f"No modelbase available. Run trainer.add_modelbases() first."
            )
        if cross_validation != 0:
            programs_predictions = self.cross_validation(
                programs=self.modelbases_names,
                n_random=cross_validation,
                verbose=verbose,
                test_data_only=test_data_only,
                load_from_previous=load_from_previous,
                split_type=split_type,
                **kwargs,
            )
        else:
            programs_predictions = {}
            for modelbase in self.modelbases:
                print(f"{modelbase.program} metrics")
                programs_predictions[modelbase.program] = modelbase._predict_all(
                    verbose=verbose, test_data_only=test_data_only
                )

        df_leaderboard = self._cal_leaderboard(
            programs_predictions, test_data_only=test_data_only
        )
        if dump_trainer:
            save_trainer(self)
        return df_leaderboard

    def get_predict_leaderboard(
        self, df: pd.DataFrame, *args, **kwargs
    ) -> pd.DataFrame:
        """
        Get prediction leaderboard of all models on an upcoming labeled dataset.

        Parameters
        ----------
        df:
            A new tabular dataset that has the same structure as ``self.trainer.datamodule.X_test``.
        args
            Arguments of :meth:`tabensemb.model.AbstractModel.predict`.
        kwargs
            Arguments of :meth:`tabensemb.model.AbstractModel.predict`.

        Returns
        -------
        pd.DataFrame
        """
        if len(self.modelbases) == 0:
            raise Exception(
                f"No modelbase available. Run trainer.add_modelbases() first."
            )
        kwargs["proba"] = True
        programs_predictions = {}
        for modelbase in self.modelbases:
            print(f"{modelbase.program} metrics")
            truth: np.ndarray = df[self.label_name].values
            program_predictions = {}
            for model_name in modelbase.get_model_names():
                pred: np.ndarray = modelbase.predict(
                    df, *args, model_name=model_name, **kwargs
                )
                program_predictions[model_name] = {"Testing": (pred, truth)}
            programs_predictions[modelbase.program] = program_predictions
        df_leaderboard = self._cal_leaderboard(
            programs_predictions, test_data_only=True
        )
        return df_leaderboard

    def get_approx_cv_leaderboard(
        self, leaderboard: pd.DataFrame, save: bool = True
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Calculate approximated averages and standard errors based on :meth:`cross_validation` results in the folder
        ``self.project_root/cv``.

        Parameters
        ----------
        leaderboard
            A reference leaderboard to be filled by avg and std, and to sort the returned DataFrame.
        save
            Save returned results locally with names "leaderboard_approx_mean.csv" and "leaderboard_approx_std.csv"

        Returns
        -------
        pd.DataFrame
            Averages in the same format as the input ``leaderboard``. There is an additional column "Rank".
        pd.DataFrame
            Standard errors in the same format as the input ``leaderboard``. There is an additional column "Rank".

        Notes
        -----
        The returned results are approximations of the precise leaderboard from ``get_leaderboard``. Some metrics like
        RMSE may be different because data-point-wise and cross-validation-wise averaging are different.
        """
        leaderboard_mean = leaderboard.copy()
        leaderboard_std = leaderboard.copy()
        leaderboard_mean["Rank"] = np.nan
        leaderboard_std["Rank"] = np.nan
        if not os.path.exists(os.path.join(self.project_root, "cv")):
            warnings.warn(
                f"Cross validation folder {os.path.join(self.project_root, 'cv')} not found."
            )
            leaderboard_mean["Rank"] = leaderboard.index.values + 1
            leaderboard_std.loc[
                :, np.setdiff1d(leaderboard_std.columns, ["Program", "Model"])
            ] = 0
            return leaderboard_mean, leaderboard_std
        df_cvs, programs, models, metrics = self._read_cv_leaderboards()
        modelwise_cv = self.get_modelwise_cv_metrics()
        for program in programs:
            program_models = models[program]
            for model in program_models:
                res_cv = modelwise_cv[program][model]
                # If numeric_only=True, only "Rank" is calculated somehow.
                mean = res_cv[metrics].mean(0, numeric_only=False)
                std = res_cv[metrics].std(0, numeric_only=False)
                where_model = leaderboard_std.loc[
                    (leaderboard_std["Program"] == program)
                    & (leaderboard_std["Model"] == model)
                ].index[0]
                leaderboard_mean.loc[where_model, mean.index] = mean
                leaderboard_std.loc[where_model, std.index] = std
        if save:
            leaderboard_mean.to_csv(
                os.path.join(self.project_root, "leaderboard_approx_mean.csv"),
                index=False,
            )
            leaderboard_std.to_csv(
                os.path.join(self.project_root, "leaderboard_approx_std.csv"),
                index=False,
            )
        return leaderboard_mean, leaderboard_std

    def get_modelwise_cv_metrics(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Assemble cross-validation results in the folder ``self.project_root/cv`` for metrics of each model in each
        model base.

        Returns
        -------
        dict
            A dict of dicts where each of them contains metrics of cross-validation of one model.
        """
        df_cvs, programs, models, metrics = self._read_cv_leaderboards()
        res_cvs = {}
        for program in programs:
            res_cvs[program] = {}
            program_models = models[program]
            for model in program_models:
                res_cvs[program][model] = pd.DataFrame(
                    columns=df_cvs[0].columns, index=np.arange(len(df_cvs))
                )
                cv_metrics = np.zeros((len(df_cvs), len(metrics)))
                for cv_idx, df_cv in enumerate(df_cvs):
                    where_model = (df_cv["Program"] == program) & (
                        df_cv["Model"] == model
                    )
                    model_metrics = df_cv.loc[where_model][metrics].values.flatten()
                    cv_metrics[cv_idx, :] = model_metrics
                res_cvs[program][model][metrics] = cv_metrics
                res_cvs[program][model]["Program"] = program
                res_cvs[program][model]["Model"] = model
        return res_cvs

    def _read_cv_leaderboards(
        self,
    ) -> Tuple[List[pd.DataFrame], List[str], Dict[str, List[str]], List[str]]:
        """
        Read cross-validation leaderboards in the folder ``self.project_root/cv``.

        Returns
        -------
        list
            Cross validation leaderboards
        list
            Model base names
        dict
            Model names in each model base
        list
            Metric names.
        """
        if not os.path.exists(os.path.join(self.project_root, "cv")):
            raise Exception(
                f"Cross validation folder {os.path.join(self.project_root, 'cv')} not found."
            )
        cvs = sorted(
            [
                i
                for i in os.listdir(os.path.join(self.project_root, "cv"))
                if "leaderboard_cv" in i
            ]
        )
        df_cvs = [
            pd.read_csv(os.path.join(self.project_root, "cv", cv), index_col=0)
            for cv in cvs
        ]
        programs = list(np.unique(df_cvs[0]["Program"].values))
        models = {
            a: list(df_cvs[0].loc[np.where(df_cvs[0]["Program"] == a)[0], "Model"])
            for a in programs
        }
        for df_cv in df_cvs:
            df_cv["Rank"] = df_cv.index.values + 1
        metrics = list(np.setdiff1d(df_cvs[0].columns, ["Program", "Model"]))
        return df_cvs, programs, models, metrics

    def _cal_leaderboard(
        self,
        programs_predictions: Dict[
            str, Dict[str, Dict[str, Tuple[np.ndarray, np.ndarray]]]
        ],
        metrics: List[str] = None,
        test_data_only: bool = False,
        save: bool = True,
    ) -> pd.DataFrame:
        """
        Calculate the leaderboard based on results from :meth:`cross_validation` or
        :meth:`tabensemb.model.AbstractModel._predict_all`.

        Parameters
        ----------
        programs_predictions
            Results from :meth:`cross_validation`, or assembled results from
            :meth:`tabensemb.model.AbstractModel._predict_all`. See the source code of
            :meth:`get_leaderboard` for details.
        metrics
            The metrics that have been implemented in :func:`tabensemb.utils.utils.metric_sklearn`.
        test_data_only
            Whether to evaluate models only on testing datasets.
        save
            Whether to save the leaderboard locally and as an attribute in the :class:`Trainer`.

        Returns
        -------
        pd.DataFrame
            The leaderboard dataframe.
        """
        if metrics is None:
            metrics = {
                "regression": REGRESSION_METRICS,
                "binary": BINARY_METRICS,
                "multiclass": MULTICLASS_METRICS,
            }[self.datamodule.task]
        dfs = []
        for modelbase_name in self.modelbases_names:
            df = self._metrics(
                programs_predictions[modelbase_name],
                metrics,
                test_data_only=test_data_only,
            )
            df["Program"] = modelbase_name
            dfs.append(df)

        df_leaderboard = pd.concat(dfs, axis=0, ignore_index=True)
        sorted_by = metrics[0].upper()
        df_leaderboard.sort_values(
            f"Testing {sorted_by}" if not test_data_only else sorted_by, inplace=True
        )
        df_leaderboard.reset_index(drop=True, inplace=True)
        df_leaderboard = df_leaderboard[["Program"] + list(df_leaderboard.columns)[:-1]]
        if save:
            df_leaderboard.to_csv(os.path.join(self.project_root, "leaderboard.csv"))
            self.leaderboard = df_leaderboard
            if os.path.exists(os.path.join(self.project_root, "cv")):
                self.get_approx_cv_leaderboard(df_leaderboard, save=True)
        return df_leaderboard

    def _plot_action_subplots(
        self,
        meth_name: str,
        ls: List[str],
        ls_kwarg_name: Union[str, None],
        tqdm_active: bool = False,
        with_title: bool = False,
        titles: List[str] = None,
        fontsize: float = 12,
        xlabel: str = None,
        ylabel: str = None,
        twin_ylabel: str = None,
        get_figsize_kwargs: Dict = None,
        figure_kwargs: Dict = None,
        meth_fix_kwargs: Dict = None,
    ):
        """
        Iterate over a list to plot subplots in a single figure.

        Parameters
        ----------
        ls
            The list to be iterated.
        ls_kwarg_name
            The argument name of the components in ``ls`` when the component is passed to ``meth_name`` one by one. If
            is None, the components in ``ls`` should be dictionaries and will be unpacked and passed to the method
            ``meth_name``.
        tqdm_active
            Whether to use a tqdm progress bar.
        meth_name
            The method to plot on a subplot. It has an argument named ``ax`` which indicates the subplot.
        with_title
            Whether each subplot has a title, which is the components in ``ls`` if ``titles`` is None.
        titles
            The titles of each subplot if ``with_title`` is True.
        fontsize
            ``plt.rcParams["font.size"]``
        xlabel
            The overall xlabel.
        ylabel
            The overall ylabel.
        twin_ylabel
            The overall ylabel of the twin x-axis.
        get_figsize_kwargs
            Arguments for :func:`tabensemb.utils.utils.get_figsize`.
        figure_kwargs
            Arguments for ``plt.figure()``
        meth_fix_kwargs
            Fixed arguments of ``meth_name`` (except for ``ax`` and ``ls_kwarg_name``).

        Returns
        -------
        matplotlib.figure.Figure
            The figure that has plotted subplots.
        """
        from tqdm.auto import tqdm

        def _iterator(iterator, *args, **kwargs):
            for item in iterator:
                yield item

        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        get_figsize_kwargs_ = update_defaults_by_kwargs(
            dict(max_col=4, width_per_item=3, height_per_item=3, max_width=14),
            get_figsize_kwargs,
        )
        figsize, width, height = get_figsize(n=len(ls), **get_figsize_kwargs_)

        fig = plt.figure(figsize=figsize, **figure_kwargs_)
        plt.rcParams["font.size"] = fontsize
        tqdm = tqdm if tqdm_active else _iterator
        for idx, name in tqdm(enumerate(ls), total=len(ls)):
            ax = plt.subplot(height, width, idx + 1)
            if with_title:
                ax.set_title(
                    name if titles is None else titles[idx], {"fontsize": fontsize}
                )
            getattr(self, meth_name)(
                ax=ax,
                **({ls_kwarg_name: name} if ls_kwarg_name is not None else name),
                **meth_fix_kwargs,
            )

        ax = fig.add_subplot(111, frameon=False)
        ax.tick_params(
            labelcolor="none",
            which="both",
            top=False,
            bottom=False,
            left=False,
            right=False,
        )
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if twin_ylabel is not None:
            twin_ax = ax.twinx()
            twin_ax.set_frame_on(False)
            twin_ax.tick_params(
                labelcolor="none",
                which="both",
                top=False,
                bottom=False,
                left=False,
                right=False,
            )
            twin_ax.set_ylabel(twin_ylabel)

        return fig

    def _plot_action_get_df(
        self, imputed: bool, scaled: bool, cat_transformed: bool
    ) -> pd.DataFrame:
        """
        A wrapper of :meth:`tabensemb.data.datamodule.DataModule.get_df`.
        """
        return self.datamodule.get_df(
            imputed=imputed, scaled=scaled, cat_transformed=cat_transformed
        )

    def plot_subplots(
        self,
        ls: List[str],
        ls_kwarg_name: str,
        meth_name: str,
        with_title: bool = False,
        titles: List[str] = None,
        fontsize: float = 12,
        xlabel: str = None,
        ylabel: str = None,
        twin_ylabel: str = None,
        get_figsize_kwargs: Dict = None,
        figure_kwargs: Dict = None,
        meth_fix_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
        tqdm_active: bool = False,
    ):
        """
        Iterate over a list to plot subplots in a single figure.

        Parameters
        ----------
        ls
            The list to be iterated.
        ls_kwarg_name
            The argument name of the components in ``ls`` when the component is passed to ``meth_name``.
        meth_name
            The method to plot on a subplot. It has an argument named ``ax`` which indicates the subplot.
        with_title
            Whether each subplot has a title, which is the components in ``ls`` if ``titles`` is None.
        titles
            The titles of each subplot if ``with_title`` is True.
        fontsize
            ``plt.rcParams["font.size"]``
        xlabel
            The overall xlabel.
        ylabel
            The overall ylabel.
        twin_ylabel
            The overall ylabel of the twin x-axis.
        get_figsize_kwargs
            Arguments for :func:`tabensemb.utils.utils.get_figsize`.
        figure_kwargs
            Arguments for ``plt.figure()``
        meth_fix_kwargs
            Fixed arguments of ``meth_name`` (except for ``ax`` and ``ls_kwarg_name``).
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure, or return the ``matplotlib.figure.Figure``
            instance.
        tqdm_active
            Whether to use a tqdm progress bar.

        Returns
        -------
        matplotlib.figure.Figure
            The figure that has plotted subplots.
        """
        fig = self._plot_action_subplots(
            ls=ls,
            ls_kwarg_name=ls_kwarg_name,
            meth_name=meth_name,
            meth_fix_kwargs=meth_fix_kwargs,
            fontsize=fontsize,
            with_title=with_title,
            titles=titles,
            xlabel=xlabel,
            ylabel=ylabel,
            twin_ylabel=twin_ylabel,
            get_figsize_kwargs=get_figsize_kwargs,
            figure_kwargs=figure_kwargs,
            tqdm_active=tqdm_active,
        )

        return self._plot_action_after_plot(
            disable=False,
            ax_or_fig=fig,
            fig_name=os.path.join(self.project_root, f"subplots.pdf"),
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_truth_pred_all(
        self,
        program: str,
        fontsize=14,
        get_figsize_kwargs: Dict = None,
        figure_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
        tqdm_active: bool = False,
        **kwargs,
    ) -> Union[None, matplotlib.figure.Figure]:
        """
        Compare ground truth and prediction for all models in a model base.

        Parameters
        ----------
        program
            The selected model base.
        fontsize
            ``plt.rcParams["font.size"]``
        get_figsize_kwargs
            Arguments for :func:`tabensemb.utils.utils.get_figsize`.
        figure_kwargs
            Arguments for ``plt.figure()``
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure, or return the ``matplotlib.figure.Figure``
            instance.
        tqdm_active
            Whether to use a tqdm progress bar.
        kwargs
            Arguments for :meth:`plot_truth_pred`

        Returns
        -------
        matplotlib.figure.Figure
            The figure if ``save_show_close`` is False.
        """
        modelbase = self.get_modelbase(program)
        model_names = modelbase.get_model_names()

        savefig_kwargs_ = update_defaults_by_kwargs(
            dict(fname=os.path.join(self.project_root, program, f"truth_pred.pdf")),
            savefig_kwargs,
        )

        return self.plot_subplots(
            ls=model_names,
            ls_kwarg_name="model_name",
            meth_name="plot_truth_pred",
            meth_fix_kwargs=dict(program=program, **kwargs),
            fontsize=fontsize,
            with_title=True,
            xlabel="Ground truth",
            ylabel="Prediction",
            get_figsize_kwargs=get_figsize_kwargs,
            figure_kwargs=figure_kwargs,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs_,
            tqdm_active=tqdm_active,
        )

    def plot_truth_pred(
        self,
        program: str,
        model_name: str,
        kde_color: bool = False,
        train_val_test: str = "all",
        log_trans: bool = True,
        central_line: bool = True,
        upper_lim=9,
        ax=None,
        clr: Iterable = None,
        select_by_value_kwargs: Dict = None,
        figure_kwargs: Dict = None,
        scatter_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Compare ground truth and prediction for one model.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base
        kde_color
            Whether the scatters are colored by their KDE density. Ignored if ``train_val_test`` is "all".
        train_val_test
            Which subset to be plotted. Choose from "Training", "Validation", "Testing", and "all".
        log_trans
            Whether the label data is in log scale.
        central_line
            Whether to plot a 45-degree diagonal line.
        upper_lim
            The upper limit of x/y-axis.
        ax
            ``matplotlib.axes.Axes``
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        figure_kwargs
            Arguments for ``plt.figure()``
        scatter_kwargs
            Arguments for ``plt.scatter()``
        legend_kwargs
            Arguments for ``plt.legend()``
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        clr = global_palette if clr is None else clr
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        legend_kwargs_ = update_defaults_by_kwargs(
            dict(loc="upper left", markerscale=1.5, handlelength=0.2, handleheight=0.9),
            legend_kwargs,
        )

        if select_by_value_kwargs is not None:
            select_by_value_kwargs_ = update_defaults_by_kwargs(
                dict(), select_by_value_kwargs
            )
            df = self._plot_action_get_df(
                imputed=True, scaled=False, cat_transformed=True
            )
            indices = self.datamodule.select_by_value(**select_by_value_kwargs_)
            df = df.loc[indices, :].reset_index(drop=True)
            derived_data = self.datamodule.get_derived_data_slice(
                derived_data=self.derived_data, indices=indices
            )
            train_val_test = "User"
            prediction = {
                "User": (
                    self.get_modelbase(program)._predict(
                        df=df, model_name=model_name, derived_data=derived_data
                    ),
                    df[self.label_name].values,
                )
            }
        else:
            prediction = self.get_modelbase(program)._predict_model(
                model_name=model_name,
                test_data_only=False if train_val_test != "Testing" else True,
            )

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        def plot_one(name, color, marker):
            pred_y, y = prediction[name]
            r2 = metric_sklearn(y, pred_y, "r2")
            loss = metric_sklearn(y, pred_y, "mse")
            print(f"{name} MSE Loss: {loss:.4f}, R2: {r2:.4f}")
            final_y = 10**y if log_trans else y
            final_y_pred = 10**pred_y if log_trans else pred_y
            if kde_color:
                xy = np.hstack([final_y, final_y_pred]).T
                z = st.gaussian_kde(xy)(xy)
                scatter_kwargs_ = update_defaults_by_kwargs(
                    scatter_kwargs, dict(c=z, color=None)
                )
            else:
                scatter_kwargs_ = update_defaults_by_kwargs(
                    dict(color=color), scatter_kwargs
                )
            scatter_kwargs_ = update_defaults_by_kwargs(
                dict(
                    s=20,
                    marker=marker,
                    label=f"{name} dataset ($R^2$={r2:.3f})",
                    linewidth=0.4,
                    edgecolors="k",
                ),
                scatter_kwargs_,
            )
            ax.scatter(final_y, final_y_pred, **scatter_kwargs_)

        if train_val_test == "all":
            plot_one("Training", clr[0], "o")
            plot_one("Validation", clr[1], "o")
            plot_one("Testing", clr[2], "o")
        else:
            plot_one(train_val_test, clr[0], "o")

        if log_trans:
            ax.set_xscale("log")
            ax.set_yscale("log")

            if central_line:
                ax.plot(
                    np.linspace(0, 10**upper_lim, 100),
                    np.linspace(0, 10**upper_lim, 100),
                    "--",
                    c="grey",
                    alpha=0.2,
                )
            locmin = matplotlib.ticker.LogLocator(
                base=10.0, subs=[0.1 * x for x in range(10)], numticks=20
            )

            # ax.set_aspect("equal", "box")

            ax.xaxis.set_minor_locator(locmin)
            ax.yaxis.set_minor_locator(locmin)
            ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
            ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

            ax.set_xlim(1, 10**upper_lim)
            ax.set_ylim(1, 10**upper_lim)
            ax.set_box_aspect(1)
        else:
            # ax.set_aspect("equal", "box")
            lx, rx = ax.get_xlim()
            ly, ry = ax.get_ylim()
            l = np.min([lx, ly])
            r = np.max([rx, ry])

            if central_line:
                ax.plot(
                    np.linspace(l, r, 100),
                    np.linspace(l, r, 100),
                    "--",
                    c="grey",
                    alpha=0.2,
                )

            ax.set_xlim(left=l, right=r)
            ax.set_ylim(bottom=l, top=r)
            ax.set_box_aspect(1)

        ax.legend(**legend_kwargs_)

        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root,
                program,
                f"{model_name.replace('/', '_')}_truth_pred.pdf",
            ),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel="Ground truth",
            ylabel="Prediction",
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def cal_feature_importance(
        self, program: str, model_name: str, method: str = "permutation", **kwargs
    ) -> Tuple[np.ndarray, List[str]]:
        """
        Calculate feature importance using a specified model. If the model base is a
        :class:`tabensemb.model.TorchModel`, ``captum`` or ``shap`` is called to make permutations. If the model base
        is only a :class:`tabensemb.model.AbstractModel`, the calculation will be much slower.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        method
            The method to calculate importance. "permutation" or "shap".
        kwargs
            kwargs for :meth:`tabensemb.model.AbstractModel.cal_feature_importance`

        Returns
        -------
        attr
            Values of feature importance.
        importance_names
            Corresponding feature names. If the model base is a ``TorchModel``, all features including derived unstacked
            features will be included. Otherwise, only :meth:`all_feature_names` will be considered.

        See Also
        --------
        :meth:`tabensemb.model.AbstractModel.cal_feature_importance`,
        :meth:`tabensemb.model.TorchModel.cal_feature_importance`
        """
        modelbase = self.get_modelbase(program)
        return modelbase.cal_feature_importance(
            model_name=model_name, method=method, **kwargs
        )

    def cal_shap(self, program: str, model_name: str, **kwargs) -> np.ndarray:
        """
        Calculate SHAP values using a specified model. If the model base is a :class:`tabensemb.model.TorchModel`, the
        ``shap.DeepExplainer`` is used. Otherwise, ``shap.KernelExplainer`` is called, which is much slower, and
        shap.kmeans is called to summarize the training data to 10 samples as the background data and 10 random samples
        in the testing set is explained, which will bias the results.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        kwargs
            kwargs for :meth:`tabensemb.model.AbstractModel.cal_shap`

        Returns
        -------
        attr
            The SHAP values. If the model base is a `TorchModel`, all features including derived unstacked features will
            be included. Otherwise, only :meth:`all_feature_names` will be considered.

        See Also
        --------
        :meth:`tabensemb.model.AbstractModel.cal_shap`,
        :meth:`tabensemb.model.TorchModel.cal_shap`

        """
        modelbase = self.get_modelbase(program)
        return modelbase.cal_shap(model_name=model_name, **kwargs)

    def plot_feature_importance(
        self,
        program: str,
        model_name: str,
        method: str = "permutation",
        importance: np.ndarray = None,
        feature_names: List[str] = None,
        clr: Iterable = None,
        ax=None,
        figure_kwargs: Dict = None,
        bar_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
        **kwargs,
    ) -> matplotlib.axes.Axes:
        """
        Plot feature importance of a model using :meth:`cal_feature_importance`.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        method
            The method to calculate feature importance. "permutation" or "shap".
        importance
            Passing feature importance values directly instead of calling
            :meth:`tabensemb.model.AbstractModel.cal_feature_importance` internally in this method.
        feature_names
            Names of features assigned to each `importance` value.
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        ax
            ``matplotlib.axes.Axes``
        figure_kwargs
            Arguments for ``plt.figure``
        bar_kwargs
            Arguments for ``seaborn.barplot``.
        legend_kwargs
            Arguments for ``plt.legend``
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.
        kwargs
            Other arguments of :meth:`tabensemb.model.AbstractModel.cal_feature_importance`

        Returns
        -------
        matplotlib.axes.Axes
        """
        attr, names = (
            self.cal_feature_importance(
                program=program, model_name=model_name, method=method, **kwargs
            )
            if (importance is None and feature_names is None)
            else (importance, feature_names)
        )

        bar_kwargs_ = update_defaults_by_kwargs(
            dict(linewidth=1, edgecolor="k", orient="h", saturation=1), bar_kwargs
        )
        figure_kwargs_ = update_defaults_by_kwargs(dict(figsize=(7, 4)), figure_kwargs)

        where_effective = np.abs(attr) > 1e-5
        effective_names = np.array(names)[where_effective]
        not_effective = list(np.setdiff1d(names, effective_names))
        if len(not_effective) > 0:
            print(f"Feature importance less than 1e-5: {not_effective}")
        attr = attr[where_effective]

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        df = pd.DataFrame(columns=["feature", "attr", "clr"])
        df["feature"] = effective_names
        df["attr"] = np.abs(attr) / np.sum(np.abs(attr))
        df.sort_values(by="attr", inplace=True, ascending=False)
        df.reset_index(drop=True, inplace=True)

        ax.set_axisbelow(True)
        x = df["feature"].values
        y = df["attr"].values

        clr = global_palette if clr is None else clr
        palette = self._plot_action_generate_feature_types_palette(clr=clr, features=x)

        # ax.set_facecolor((0.97,0.97,0.97))
        # plt.grid(axis='x')
        plt.grid(axis="x", linewidth=0.2)
        # plt.barh(x,y, color= [clr_map[name] for name in x])
        sns.barplot(x=y, y=x, palette=palette, ax=ax, **bar_kwargs_)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        # ax.set_xlim([0, 1])

        legend = self._plot_action_generate_feature_types_legends(
            clr=clr, ax=ax, legend_kwargs=legend_kwargs
        )
        legend.get_frame().set_alpha(None)
        legend.get_frame().set_facecolor([1, 1, 1, 0.4])

        if method == "permutation":
            xlabel = "Permutation feature importance"
        elif method == "shap":
            xlabel = "SHAP feature importance"
        else:
            xlabel = "Feature importance"
        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root,
                f"feature_importance_{program}_{model_name}_{method}.png",
            ),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=xlabel,
            ylabel=None,
            tight_layout=True,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_partial_dependence_all(
        self,
        program: str,
        model_name: str,
        fontsize=12,
        figure_kwargs: Dict = None,
        get_figsize_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
        tqdm_active: bool = False,
        **kwargs,
    ) -> Union[None, matplotlib.figure.Figure]:
        """
        Calculate and plot partial dependence plots with bootstrapping.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        fontsize
            ``plt.rcParams["font.size"]``
        figure_kwargs
            Arguments for ``plt.figure``.
        get_figsize_kwargs
            Arguments for :func:`tabensemb.utils.utils.get_figsize`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure, or return the ``matplotlib.figure.Figure``
            instance.
        tqdm_active
            Whether to use a tqdm progress bar.
        kwargs
            Arguments for :meth:`plot_partial_dependence`.

        Returns
        -------
        matplotlib.figure.Figure
            The figure if ``save_show_close`` is False.
        """
        savefig_kwargs_ = update_defaults_by_kwargs(
            dict(
                fname=os.path.join(
                    self.project_root, f"partial_dependence_{program}_{model_name}.pdf"
                )
            ),
            savefig_kwargs,
        )

        return self.plot_subplots(
            ls=self.all_feature_names,
            ls_kwarg_name="feature",
            meth_name="plot_partial_dependence",
            meth_fix_kwargs=dict(program=program, model_name=model_name, **kwargs),
            fontsize=fontsize,
            with_title=True,
            xlabel=r"Value of predictors ($10\%$-$90\%$ percentile)",
            ylabel="Predicted target",
            get_figsize_kwargs=get_figsize_kwargs,
            figure_kwargs=figure_kwargs,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs_,
            tqdm_active=tqdm_active,
        )

    def plot_partial_dependence(
        self,
        program: str,
        model_name: str,
        feature: str,
        ax=None,
        refit: bool = True,
        log_trans: bool = True,
        lower_lim: float = 2,
        upper_lim: float = 7,
        n_bootstrap: int = 1,
        grid_size: int = 30,
        CI: float = 0.95,
        verbose: bool = True,
        figure_kwargs: Dict = None,
        plot_kwargs: Dict = None,
        fill_between_kwargs: Dict = None,
        bar_kwargs: Dict = None,
        hist_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Calculate and plot a partial dependence plot with bootstrapping for a feature.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        feature
            The selected feature to calculate partial dependence.
        ax
            ``matplotlib.axes.Axes``
        refit
            Whether to refit models on bootstrapped datasets. See :meth:`_bootstrap_fit`.
        log_trans
            Whether the label data is in log scale.
        lower_lim
            Lower limit of all pdp plots.
        upper_lim
            Upper limit of all pdp plot.
        n_bootstrap
            The number of bootstrap evaluations. It should be greater than 0.
        grid_size
            The number of steps of all pdp plot.
        CI
            The confidence interval of pdp results calculated across multiple bootstrap runs.
        verbose
            Verbosity
        figure_kwargs
            Arguments for ``plt.figure``.
        plot_kwargs
            Arguments for ``ax.plot``.
        fill_between_kwargs
            Arguments for ``ax.fill_between``.
        bar_kwargs
            Arguments for ``ax.bar`` (used for frequencies of categorical features).
        hist_kwargs
            Arguments for ``ax.hist`` (used for histograms of continuous features).
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        (
            x_values_list,
            mean_pdp_list,
            ci_left_list,
            ci_right_list,
        ) = self.cal_partial_dependence(
            feature_subset=[feature],
            program=program,
            model_name=model_name,
            df=self.datamodule.X_train,
            derived_data=self.datamodule.D_train,
            n_bootstrap=n_bootstrap,
            refit=refit,
            grid_size=grid_size,
            percentile=90,
            CI=CI,
            average=True,
        )
        x_values = x_values_list[0]
        mean_pdp = mean_pdp_list[0]
        ci_left = ci_left_list[0]
        ci_right = ci_right_list[0]

        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        plot_kwargs_ = update_defaults_by_kwargs(
            dict(color="k", linewidth=0.7), plot_kwargs
        )
        fill_between_kwargs_ = update_defaults_by_kwargs(
            dict(alpha=0.4, color="k", edgecolor=None), fill_between_kwargs
        )

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        def transform(value):
            if log_trans:
                return 10**value
            else:
                return value

        if feature not in self.cat_feature_names:
            ax.plot(x_values, transform(mean_pdp), **plot_kwargs_)

            ax.fill_between(
                x_values,
                transform(ci_left),
                transform(ci_right),
                **fill_between_kwargs_,
            )
        else:
            yerr = (
                np.abs(
                    np.vstack([transform(ci_left), transform(ci_right)])
                    - transform(mean_pdp)
                )
                if not np.isnan(ci_left).any()
                else None
            )
            ax.errorbar(x_values, transform(mean_pdp), yerr=yerr, **plot_kwargs_)

        # ax.set_xlim([0, 1])
        if log_trans:
            ax.set_yscale("log")
            ax.set_ylim([10**lower_lim, 10**upper_lim])
            locmin = matplotlib.ticker.LogLocator(
                base=10.0, subs=[0.1 * x for x in range(10)], numticks=20
            )
            # ax.xaxis.set_minor_locator(locmin)
            ax.yaxis.set_minor_locator(locmin)
            # ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
            ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

        if np.min(x_values) < np.max(x_values):
            ax2 = ax.twinx()
            hist_kwargs_ = update_defaults_by_kwargs(
                dict(bins=x_values, alpha=0.2, color="k"), hist_kwargs
            )
            bar_kwargs_ = update_defaults_by_kwargs(
                dict(alpha=0.2, color="k"), bar_kwargs
            )
            self.plot_hist(
                feature=feature,
                ax=ax2,
                imputed=False,
                x_values=x_values,
                hist_kwargs=hist_kwargs_,
                bar_kwargs=bar_kwargs_,
            )
            ax2.set_yticks([])
        else:
            ax2 = ax.twinx()
            ax2.text(0.5, 0.5, "Invalid interval", ha="center", va="center")
            ax2.set_xlim([0, 1])
            ax2.set_ylim([0, 1])
            ax2.set_yticks([])

        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root,
                f"partial_dependence_{program}_{model_name}_{feature}.pdf",
            ),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=feature + r" ($10\%$-$90\%$ percentile)",
            ylabel="Predicted target",
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def cal_partial_dependence(
        self, feature_subset: List[str] = None, **kwargs
    ) -> Tuple[List[np.ndarray], List[np.ndarray], List[np.ndarray], List[np.ndarray]]:
        """
        Calculate partial dependency. See the source code of :meth:`plot_partial_dependence` for its usage.

        Parameters
        ----------
        feature_subset
            A subset of :meth:`all_feature_names`.
        kwargs
            Arguments for :meth:`_bootstrap_fit`.

        Returns
        -------
        list
            x values for each feature
        list
            pdp values for each feature
        list
            lower confidence limits for each feature
        list
            upper confidence limits for each feature
        """
        x_values_list = []
        mean_pdp_list = []
        ci_left_list = []
        ci_right_list = []

        for feature_idx, feature_name in enumerate(
            self.all_feature_names if feature_subset is None else feature_subset
        ):
            print("Calculate PDP: ", feature_name)

            x_value, model_predictions, ci_left, ci_right = self._bootstrap_fit(
                focus_feature=feature_name, **kwargs
            )

            x_values_list.append(x_value)
            mean_pdp_list.append(model_predictions)
            ci_left_list.append(ci_left)
            ci_right_list.append(ci_right)

        return x_values_list, mean_pdp_list, ci_left_list, ci_right_list

    def plot_partial_dependence_2way_all(
        self,
        program: str,
        model_name: str,
        x_feature: str,
        y_features: List[str] = None,
        fontsize=12,
        figure_kwargs: Dict = None,
        get_figsize_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
        tqdm_active: bool = False,
        **kwargs,
    ) -> Union[None, matplotlib.figure.Figure]:
        """
        Calculate and plot 2-way partial dependence plots with bootstrapping. One continuous feature is fixed for x-axis.
        The rest of the continuous features are on y-axis, respectively.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        x_feature
            The continuous feature fixed for x-axis.
        y_features
            Continuous features on y-axis respectively. If None, all other continuous features are used.
        fontsize
            ``plt.rcParams["font.size"]``
        figure_kwargs
            Arguments for ``plt.figure``.
        get_figsize_kwargs
            Arguments for :func:`tabensemb.utils.utils.get_figsize`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure, or return the ``matplotlib.figure.Figure``
            instance.
        tqdm_active
            Whether to use a tqdm progress bar.
        kwargs
            Arguments for :meth:`plot_partial_dependence_2way`.

        Returns
        -------
        matplotlib.figure.Figure
            The figure if ``save_show_close`` is False.
        """
        y_features = (
            y_features
            if y_features is not None
            else [x for x in self.cont_feature_names if x != x_feature]
        )
        savefig_kwargs_ = update_defaults_by_kwargs(
            dict(
                fname=os.path.join(
                    self.project_root,
                    f"partial_dependence_2way_{program}_{model_name}_{x_feature}.pdf",
                )
            ),
            savefig_kwargs,
        )

        return self.plot_subplots(
            ls=y_features,
            ls_kwarg_name="y_feature",
            meth_name="plot_partial_dependence_2way",
            meth_fix_kwargs=dict(
                x_feature=x_feature, program=program, model_name=model_name, **kwargs
            ),
            fontsize=fontsize,
            with_title=True,
            xlabel=r"Value of the fixed predictors",
            ylabel="Value of other predictors",
            get_figsize_kwargs=get_figsize_kwargs,
            figure_kwargs=figure_kwargs,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs_,
            tqdm_active=tqdm_active,
        )

    def plot_partial_dependence_2way(
        self,
        x_feature: str,
        y_feature: str,
        program: str,
        model_name: str,
        df: pd.DataFrame,
        derived_data: Dict[str, np.ndarray],
        ax: matplotlib.axes.Axes = None,
        projection: str = "3d",
        grid_size: int = 10,
        percentile: Union[int, float] = 100,
        figure_kwargs: Dict = None,
        imshow_kwargs: Dict = None,
        surf_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
        **kwargs,
    ):
        """
        Calculate and plot a 2-way partial dependence plot with bootstrapping for a pair of features.

        Parameters
        ----------
        x_feature
            A continuous feature.
        y_feature
            A continuous feature.
        program
            The selected model base.
        model_name
            The selected model in the model base.
        ax
            ``matplotlib.axes.Axes``
        projection
            None or "3d". Will use ``matplotlib.pyplot.imshow`` for None and ``matplotlib.pyplot.plot_surface`` for "3d".
        grid_size
            The number of sequential values.
        percentile
            The percentile of the feature used to generate sequential values.
        df
            The tabular dataset.
        derived_data
            The derived data calculated using :meth:`derive_unstacked`.
        kwargs
            Other arguments for :meth:`cal_partial_dependence_2way`.
        figure_kwargs
            Arguments for ``plt.savefig``
        savefig_kwargs
            Arguments for ``plt.savefig``
        imshow_kwargs
            Arguments for ``plt.imshow``
        surf_kwargs
            Arguments for ``plt.plot_surface``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.
        kwargs
            Arguments for :meth:`cal_partial_dependence_2way`.

        Returns
        -------
        matplotlib.axes.Axes
        """
        from matplotlib import cm

        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        imshow_kwargs_ = update_defaults_by_kwargs(dict(), imshow_kwargs)
        surf_kwargs_ = update_defaults_by_kwargs(
            dict(cmap=cm.coolwarm, linewidth=0, antialiased=False), surf_kwargs
        )

        given_ax = ax is not None
        if not given_ax:
            fig = plt.figure(**figure_kwargs_)
            ax = plt.subplot(111, projection=projection)
        plt.sca(ax)

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        X, Y, Z = self.cal_partial_dependence_2way(
            x_feature=x_feature,
            y_feature=y_feature,
            grid_size=grid_size,
            percentile=percentile,
            program=program,
            model_name=model_name,
            derived_data=derived_data,
            df=df,
            **kwargs,
        )

        if projection != "3d":
            ax.imshow(np.rot90(Z), **imshow_kwargs_)
            ax.set_xticks(np.arange(len(X)))
            ax.set_yticks(np.arange(len(Y)))
            ax.set_xticklabels([round(x, 2) for x in X[:, 0]])
            ax.set_yticklabels([round(x, 2) for x in Y[0, ::-1]])
        else:
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.xaxis.pane.set_edgecolor("w")
            ax.yaxis.pane.set_edgecolor("w")
            ax.zaxis.pane.set_edgecolor("w")
            surf = ax.plot_surface(X, Y, Z, **surf_kwargs_)

        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root,
                f"partial_dependence_2way_{program}_{model_name}_{x_feature}_{y_feature}.pdf",
            ),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=x_feature
            + r" (${}\%$-${}\%$ percentile)".format(100 - percentile, percentile),
            ylabel=y_feature
            + r" (${}\%$-${}\%$ percentile)".format(100 - percentile, percentile),
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def cal_partial_dependence_2way(
        self,
        x_feature: str,
        y_feature: str,
        grid_size: int = 10,
        percentile: Union[int, float] = 100,
        x_min: Union[int, float] = None,
        x_max: Union[int, float] = None,
        y_min: Union[int, float] = None,
        y_max: Union[int, float] = None,
        df: pd.DataFrame = None,
        **kwargs,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate 2-way partial dependency. See the source code of :meth:`plot_partial_dependence_2way` for its usage.

        Parameters
        ----------
        x_feature
            A continuous feature.
        y_feature
            A continuous feature.
        grid_size
            The number of sequential values.
        percentile
            The percentile of the feature used to generate sequential values.
        x_min
            The lower limit of the generated sequential values of the first feature.
            It will override the left percentile.
        x_max
            The upper limit of the generated sequential values of the first feature.
            It will override the right percentile.
        y_min
            The lower limit of the generated sequential values of the second feature.
            It will override the left percentile.
        y_max
            The upper limit of the generated sequential values of the second feature.
            It will override the right percentile.
        df
            The tabular dataset.
        kwargs
            Other arguments for :meth:`_bootstrap_fit`. The above `grid_size`, `percentile`, `y_min`, `y_max` are
            passed to it for the second feature.

        Returns
        -------
        list
            The grid of the first feature
        list
            The grid of the second feature
        list
            pdp values of each first-feature value and each second-feature value in grids.
        """
        y_values_list = []
        mean_pdp_list = []
        df = df if df is not None else self.df
        df = df.copy()
        x_values_list = list(
            self._generate_grid(
                feature=x_feature,
                grid_size=grid_size,
                percentile=percentile,
                x_min=x_min,
                x_max=x_max,
                df=df,
            )
        )

        for x_val in x_values_list:
            df[x_feature] = x_val
            x_value, model_predictions, _, _ = self._bootstrap_fit(
                focus_feature=y_feature,
                df=df,
                grid_size=grid_size,
                percentile=percentile,
                x_min=y_min,
                x_max=y_max,
                **kwargs,
            )

            y_values_list.append(x_value)
            mean_pdp_list.append(model_predictions)

        return (
            np.repeat(np.array(x_values_list).reshape(1, -1), grid_size, axis=0).T,
            np.array(y_values_list),
            np.array(mean_pdp_list),
        )

    def plot_partial_err_all(
        self,
        program: str,
        model_name: str,
        fontsize=12,
        figure_kwargs: Dict = None,
        get_figsize_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
        tqdm_active: bool = False,
        **kwargs,
    ) -> Union[None, matplotlib.figure.Figure]:
        """
        Calculate prediction absolute errors on the testing dataset, and plot histograms of high-error samples and
        low-error samples respectively.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        fontsize
            ``plt.rcParams["font.size"]``
        figure_kwargs
            Arguments for ``plt.figure``.
        get_figsize_kwargs
            Arguments for :func:`tabensemb.utils.utils.get_figsize`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure, or return the ``matplotlib.figure.Figure``
            instance.
        tqdm_active
            Whether to use a tqdm progress bar.
        kwargs
            Arguments for :meth:`plot_partial_err`

        Returns
        -------
        matplotlib.figure.Figure
            The figure if ``save_show_close`` is False.
        """
        savefig_kwargs_ = update_defaults_by_kwargs(
            dict(
                fname=os.path.join(
                    self.project_root, f"partial_err_{program}_{model_name}.pdf"
                )
            ),
            savefig_kwargs,
        )

        return self.plot_subplots(
            ls=self.all_feature_names,
            ls_kwarg_name="feature",
            meth_name="plot_partial_err",
            meth_fix_kwargs=dict(program=program, model_name=model_name, **kwargs),
            fontsize=fontsize,
            with_title=True,
            xlabel="Value of predictors",
            ylabel="Prediction absolute error",
            get_figsize_kwargs=get_figsize_kwargs,
            figure_kwargs=figure_kwargs,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs_,
            tqdm_active=tqdm_active,
        )

    def plot_partial_err(
        self,
        program: str,
        model_name: str,
        feature,
        thres=0.8,
        ax=None,
        clr: Iterable = None,
        figure_kwargs: Dict = None,
        scatter_kwargs: Dict = None,
        hist_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Calculate prediction absolute errors on the testing dataset, and plot histograms of high-error samples and
        low-error samples respectively for a single feature.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        feature
            The selected feature.
        thres
            The absolute error threshold to identify high-error samples and low-error samples.
        ax
            ``matplotlib.axes.Axes``
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        figure_kwargs
            Arguments for ``plt.figure``.
        scatter_kwargs
            Arguments for ``ax.scatter()``
        hist_kwargs
            Arguments for ``ax.hist()``
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        clr = global_palette if clr is None else clr
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        scatter_kwargs_ = update_defaults_by_kwargs(dict(s=1), scatter_kwargs)
        hist_kwargs_ = update_defaults_by_kwargs(
            dict(density=True, alpha=0.2, rwidth=0.8), hist_kwargs
        )

        feature_data = self.df.loc[
            np.array(self.test_indices), self.all_feature_names
        ].reset_index(drop=True)

        truth = self.label_data.loc[self.test_indices, :].values.flatten()
        modelbase = self.get_modelbase(program)
        pred = modelbase.predict(
            df=self.datamodule.X_test,
            derived_data=self.datamodule.D_test,
            model_name=model_name,
        ).flatten()
        err = np.abs(truth - pred)
        high_err_data = feature_data.loc[np.where(err > thres)[0], :]
        high_err = err[np.where(err > thres)[0]]
        low_err_data = feature_data.loc[np.where(err <= thres)[0], :]
        low_err = err[np.where(err <= thres)[0]]

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        ax.scatter(
            high_err_data[feature].values,
            high_err,
            color=clr[0],
            marker="s",
            **scatter_kwargs_,
        )
        ax.scatter(
            low_err_data[feature].values,
            low_err,
            color=clr[1],
            marker="^",
            **scatter_kwargs_,
        )

        ax.set_ylim([0, np.max(err) * 1.1])
        ax2 = ax.twinx()

        ax2.hist(
            [
                high_err_data[feature].values,
                low_err_data[feature].values,
            ],
            bins=np.linspace(
                np.min(feature_data[feature].values),
                np.max(feature_data[feature].values),
                20,
            ),
            color=clr[:2],
            **hist_kwargs_,
        )
        if feature in self.cat_feature_names:
            ticks = np.sort(np.unique(feature_data[feature].values)).astype(int)
            tick_label = [self.cat_feature_mapping[feature][x] for x in ticks]
            ax.set_xticks(ticks)
            ax.set_xticklabels(tick_label)
            ax.set_xlim([-0.5, len(ticks) - 0.5])
            ax2.set_xlim([-0.5, len(ticks) - 0.5])

        # sns.rugplot(data=chosen_data, height=0.05, ax=ax2, color='k')
        # ax2.set_ylim([0,1])
        # ax2.set_xlim([np.min(x_values_list[idx]), np.max(x_values_list[idx])])
        ax2.set_yticks([])

        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root, f"partial_err_{program}_{model_name}_{feature}.pdf"
            ),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=feature,
            ylabel="Prediction absolute error",
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_err_hist(
        self,
        program: str,
        model_name: str,
        category: str = None,
        metric: str = None,
        ax=None,
        legend=True,
        clr: Iterable = None,
        figure_kwargs: Dict = None,
        hist_kwargs: Dict = None,
        select_by_value_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot histograms of prediction errors.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        category
            The category to classify histograms and stack them with different colors.
        metric
            The metric to be calculated. It should be supported by :func:`tabenseb.utils.utils.auto_metric_sklearn`.
        ax
            ``matplotlib.axes.Axes``
        legend
            Show legends if ``category`` is not None.
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        figure_kwargs
            Arguments for ``plt.figure``.
        hist_kwargs
            Arguments for ``ax.hist`` (used for histograms of continuous features).
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        legend_kwargs
            Arguments for ``plt.legend`` if ``legend`` is True and ``category`` is not None.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        clr = global_palette if clr is None else clr
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        select_by_value_kwargs_ = update_defaults_by_kwargs(
            dict(), select_by_value_kwargs
        )
        hist_kwargs_ = update_defaults_by_kwargs(
            dict(density=True, color=clr[0], rwidth=0.95, bins=20), hist_kwargs
        )
        legend_kwargs_ = update_defaults_by_kwargs(dict(), legend_kwargs)

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        indices = self.datamodule.select_by_value(**select_by_value_kwargs_)
        df = self._plot_action_get_df(
            imputed=True, scaled=False, cat_transformed=False
        ).loc[indices, :]
        derived_data = self.datamodule.get_derived_data_slice(
            self.datamodule.derived_data, indices=indices
        )
        pred = self.get_modelbase(program=program).predict(
            df=df, model_name=model_name, derived_data=derived_data, proba=True
        )
        truth = df[self.label_name].values

        metric = (
            metric
            if metric is not None
            else ("rmse" if self.datamodule.task == "regression" else "log_loss")
        )
        metrics = np.array(
            [
                auto_metric_sklearn(
                    t,
                    p,
                    metric=metric,
                    task=self.datamodule.task,
                )
                for t, p in zip(truth, pred)
            ]
        )

        if category is not None:
            category_data, unique_values = self._plot_action_category_unique_values(
                df=df, category=category
            )
            metrics = [
                metrics[np.where(category_data == val)[0]] for val in unique_values
            ]
            hist_kwargs_.update(
                dict(
                    color=clr[: len(unique_values)],
                    label=unique_values.astype(str),
                    stacked=True,
                )
            )

        ax.hist(metrics, **hist_kwargs_)
        if legend:
            ax.legend(**legend_kwargs_)

        return self._plot_action_after_plot(
            fig_name=os.path.join(self.project_root, f"err_hist.pdf"),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=metric.upper(),
            ylabel="Density" if hist_kwargs_["density"] else "Frequency",
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_corr(
        self,
        fontsize: Any = 10,
        imputed=False,
        features: List[str] = None,
        method: Union[str, Callable] = "pearson",
        include_label: bool = True,
        ax=None,
        figure_kwargs: Dict = None,
        imshow_kwargs: Dict = None,
        select_by_value_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot correlation coefficients among features and the target.

        Parameters
        ----------
        fontsize
            The ``fontsize`` argument for matplotlib.
        imputed
            Whether the imputed dataset should be considered. If False, some NaN coefficients may exist for features
            with missing values.
        features
            A subset of continuous features to calculate correlations on.
        method
            The argument of ``pd.DataFrame.corr``. "pearson", "kendall", "spearman" or Callable.
        include_label
            If True, the target is also considered.
        ax
            ``matplotlib.axes.Axes``
        figure_kwargs
            Arguments for ``plt.figure``.
        imshow_kwargs
            Arguments for ``plt.imshow``.
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        figure_kwargs_ = update_defaults_by_kwargs(
            dict(figsize=(10, 10)), figure_kwargs
        )
        imshow_kwargs_ = update_defaults_by_kwargs(dict(cmap="bwr"), imshow_kwargs)

        cont_feature_names = (
            self.cont_feature_names if features is None else features
        ) + (self.label_name if include_label else [])
        # sns.reset_defaults()
        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)
        plt.box(on=True)
        corr = (
            self.datamodule.cal_corr(
                method=method,
                imputed=imputed,
                features_only=False,
                select_by_value_kwargs=select_by_value_kwargs,
            )
            .loc[cont_feature_names, cont_feature_names]
            .values
        )
        im = ax.imshow(corr, **imshow_kwargs_)
        ax.set_xticks(np.arange(len(cont_feature_names)))
        ax.set_yticks(np.arange(len(cont_feature_names)))

        ax.set_xticklabels(cont_feature_names, fontsize=fontsize)
        ax.set_yticklabels(cont_feature_names, fontsize=fontsize)

        plt.setp(
            ax.get_xticklabels(),
            rotation=90,
            va="center",
            ha="right",
            rotation_mode="anchor",
        )

        norm_corr = corr - (np.nanmax(corr) + np.nanmin(corr)) / 2
        norm_corr /= np.nanmax(norm_corr)

        for i in range(len(cont_feature_names)):
            for j in range(len(cont_feature_names)):
                text = ax.text(
                    j,
                    i,
                    round(corr[i, j], 2),
                    ha="center",
                    va="center",
                    color="w" if np.abs(norm_corr[i, j]) > 0.3 else "k",
                    fontsize=fontsize,
                )

        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root, f"corr{'_imputed' if imputed else ''}.pdf"
            ),
            disable=given_ax,
            ax_or_fig=ax,
            tight_layout=True,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_corr_with_label(
        self,
        imputed=False,
        features: List[str] = None,
        order: str = "alphabetic",
        method: str = "pearson",
        clr=None,
        ax=None,
        figure_kwargs: Dict = None,
        barplot_kwargs: Dict = None,
        select_by_value_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot correlation coefficients between the target and each feature.

        Parameters
        ----------
        imputed
            Whether the imputed dataset should be considered. If False, some NaN coefficients may exist for features
            with missing values.
        features
            A subset of continuous features to calculate correlations on.
        order
            The order of features. "alphabetic", "ascending", or "descending".
        method
            The argument of ``pd.DataFrame.corr``. "pearson", "kendall", "spearman" or Callable.
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        ax
            ``matplotlib.axes.Axes``
        figure_kwargs
            Arguments for ``plt.figure``.
        imshow_kwargs
            Arguments for ``plt.imshow``.
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        legend_kwargs
            Arguments for ``plt.legend``
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        figure_kwargs_ = update_defaults_by_kwargs(dict(figsize=(8, 5)), figure_kwargs)
        barplot_kwargs_ = update_defaults_by_kwargs(
            dict(
                orient="h",
                linewidth=1,
                edgecolor="k",
                saturation=1,
            ),
            barplot_kwargs,
        )
        legend_kwargs_ = update_defaults_by_kwargs(dict(), legend_kwargs)

        is_horizontal = barplot_kwargs_["orient"] == "h"

        cont_feature_names = self.cont_feature_names if features is None else features

        # sns.reset_defaults()
        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)
        plt.box(on=True)
        corr = (
            self.datamodule.cal_corr(
                method=method,
                imputed=imputed,
                features_only=False,
                select_by_value_kwargs=select_by_value_kwargs,
            )
            .loc[cont_feature_names, self.label_name]
            .values.flatten()
        )
        df = pd.DataFrame(data={"feature": cont_feature_names, "correlation": corr})
        df.sort_values(
            by="feature" if order == "alphabetic" else "correlation",
            ascending=order != "descending",
            inplace=True,
        )

        clr = global_palette if clr is None else clr
        palette = self._plot_action_generate_feature_types_palette(
            clr=clr, features=df["feature"]
        )

        sns.barplot(
            data=df,
            x="correlation" if is_horizontal else "feature",
            y="feature" if is_horizontal else "correlation",
            ax=ax,
            palette=palette,
            **barplot_kwargs_,
        )
        ax.set_xlabel(None)
        ax.set_ylabel(None)

        legend = self._plot_action_generate_feature_types_legends(
            clr=clr, ax=ax, legend_kwargs=legend_kwargs_
        )

        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root, f"corr_with_label{'_imputed' if imputed else ''}.pdf"
            ),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=f"Correlation with {self.label_name[0]}" if is_horizontal else None,
            ylabel=(
                f"Correlation with {self.label_name[0]}" if not is_horizontal else None
            ),
            tight_layout=True,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_pairplot(
        self,
        imputed: bool = False,
        features: List[str] = None,
        include_label=True,
        pairplot_kwargs: Dict = None,
        select_by_value_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> Union[None, sns.axisgrid.PairGrid]:
        """
        Plot ``seaborn.pairplot`` among features and label. Kernel Density Estimation plots are on the diagonal.

        Parameters
        ----------
        imputed
            Whether the imputed dataset should be considered.
        features
            A subset of continuous features to plot pairplots for.
        include_label
            If True, the target is also considered.
        pairplot_kwargs
            Arguments for ``seaborn.pairplot``.
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure, or return the ``seaborn.axisgrid.PairGrid``
            instance.
        """
        pairplot_kwargs_ = update_defaults_by_kwargs(
            dict(corner=True, diag_kind="kde"), pairplot_kwargs
        )
        select_by_value_kwargs_ = update_defaults_by_kwargs(
            dict(), select_by_value_kwargs
        )

        cont_feature_names = (
            self.cont_feature_names if features is None else features
        ) + (self.label_name if include_label else [])
        df_all = self._plot_action_get_df(
            imputed=imputed, scaled=False, cat_transformed=False
        )[cont_feature_names]
        indices = self.datamodule.select_by_value(**select_by_value_kwargs_)
        grid = sns.pairplot(df_all.loc[indices, :], **pairplot_kwargs_)

        return self._plot_action_after_plot(
            fig_name=os.path.join(self.project_root, "pair.jpg"),
            disable=False,
            ax_or_fig=grid,
            tight_layout=True,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_feature_box(
        self,
        imputed: bool = False,
        features: List[str] = None,
        ax=None,
        clr: Iterable = None,
        figure_kwargs: Dict = None,
        boxplot_kwargs: Dict = None,
        select_by_value_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot boxplot of the tabular data.

        Parameters
        ----------
        imputed
            Whether the imputed dataset should be considered.
        ax
            ``matplotlib.axes.Axes``
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        figure_kwargs
            Arguments for ``plt.figure``
        boxplot_kwargs
            Arguments for ``seaborn.boxplot``
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        clr = global_palette if clr is None else clr
        figure_kwargs_ = update_defaults_by_kwargs(dict(figsize=(6, 6)), figure_kwargs)
        boxplot_kwargs_ = update_defaults_by_kwargs(
            dict(
                orient="h",
                linewidth=1,
                fliersize=2,
                flierprops={"marker": "o"},
                color=clr[0],
                saturation=1,
            ),
            boxplot_kwargs,
        )
        select_by_value_kwargs_ = update_defaults_by_kwargs(
            dict(), select_by_value_kwargs
        )
        indices = self.datamodule.select_by_value(**select_by_value_kwargs_)

        # sns.reset_defaults()
        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)
        data = self._plot_action_get_df(
            imputed=imputed, scaled=True, cat_transformed=False
        )[self.cont_feature_names if features is None else features]
        bp = sns.boxplot(
            data=data.loc[indices, :],
            ax=ax,
            **boxplot_kwargs_,
        )
        ax.set_ylabel(None)
        ax.set_xlabel(None)

        boxes = []

        for x in ax.get_children():
            if isinstance(x, matplotlib.patches.PathPatch):
                boxes.append(x)

        for patch in boxes:
            patch.set_facecolor(clr[0])

        plt.grid(linewidth=0.4, axis="x")
        ax.set_axisbelow(True)
        # ax.tick_params(axis='x', rotation=90)
        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root, f"feature_box{'_imputed' if imputed else ''}.pdf"
            ),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel="Values (Scaled)",
            ylabel=None,
            tight_layout=True,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_hist_all(
        self,
        imputed=False,
        fontsize=12,
        get_figsize_kwargs: Dict = None,
        figure_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
        tqdm_active: bool = False,
        **kwargs,
    ) -> matplotlib.figure.Figure:
        """
        Plot histograms of the tabular data.

        Parameters
        ----------
        imputed
            Whether the imputed dataset should be considered.
        figure_kwargs
            Arguments for ``plt.figure``.
        fontsize
            ``plt.rcParams["font.size"]``
        get_figsize_kwargs
            Arguments for :func:`tabensemb.utils.utils.get_figsize`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure, or return the ``matplotlib.figure.Figure``
            instance.
        tqdm_active
            Whether to use a tqdm progress bar.
        **kwargs
            Arguments for :meth:`plot_hist`.

        Returns
        -------
        matplotlib.figure.Figure
            The figure if ``save_show_close`` is False.
        """
        savefig_kwargs_ = update_defaults_by_kwargs(
            dict(
                fname=os.path.join(
                    self.project_root, f"hist{'_imputed' if imputed else ''}.pdf"
                )
            ),
            savefig_kwargs,
        )

        return self.plot_subplots(
            ls=self.all_feature_names + self.label_name,
            ls_kwarg_name="feature",
            meth_name="plot_hist",
            meth_fix_kwargs=dict(imputed=imputed, **kwargs),
            fontsize=fontsize,
            with_title=True,
            xlabel="Value of predictors",
            ylabel="Density",
            get_figsize_kwargs=get_figsize_kwargs,
            figure_kwargs=figure_kwargs,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs_,
            tqdm_active=tqdm_active,
        )

    def plot_hist(
        self,
        feature: str,
        ax=None,
        clr: Iterable = None,
        imputed=False,
        kde=False,
        category: str = None,
        x_values=None,
        legend: bool = True,
        figure_kwargs: Dict = None,
        hist_kwargs: Dict = None,
        bar_kwargs: Dict = None,
        select_by_value_kwargs: Dict = None,
        kde_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot the histogram of a feature.

        Parameters
        ----------
        feature
            The selected feature.
        ax
            ``matplotlib.axes.Axes``
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        imputed
            Whether the imputed dataset should be considered.
        kde
            Plot the kernel density estimation along with each histogram of continuous features.
        category
            The category to classify histograms and stack them with different colors.
        x_values
            Unique values of the `feature`. If None, it will be inferred from the dataset.
        legend
            Show legends if ``category`` is not None.
        figure_kwargs
            Arguments for ``plt.figure``.
        bar_kwargs
            Arguments for ``ax.bar`` (used for frequencies of categorical features).
        hist_kwargs
            Arguments for ``ax.hist`` (used for histograms of continuous features).
        kde_kwargs
            Arguments for :meth:`plot_kde` when ``kde`` is True.
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        legend_kwargs
            Arguments for ``plt.legend`` if ``legend`` is True and ``category`` is not None.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        clr = global_palette if clr is None else clr
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        select_by_value_kwargs_ = update_defaults_by_kwargs(
            dict(), select_by_value_kwargs
        )
        kde_kwargs_ = update_defaults_by_kwargs(
            dict(imputed=imputed, select_by_value_kwargs=select_by_value_kwargs_),
            kde_kwargs,
        )
        legend_kwargs_ = update_defaults_by_kwargs(dict(), legend_kwargs)

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        hist_data = self._plot_action_get_df(
            imputed=imputed, scaled=False, cat_transformed=True
        )
        indices = self.datamodule.select_by_value(**select_by_value_kwargs_)
        hist_data = hist_data.loc[indices, :].reset_index(drop=True)
        bar_kwargs_ = update_defaults_by_kwargs(
            dict(color=clr[0], edgecolor=None), bar_kwargs
        )
        hist_kwargs_ = update_defaults_by_kwargs(
            dict(density=True, color=clr[0], rwidth=0.95, stacked=True), hist_kwargs
        )
        x_values = (
            np.sort(np.unique(hist_data[feature].values.flatten()))
            if x_values is None
            else x_values
        )
        x_values = x_values[np.isfinite(x_values)]
        category_data, category_unique_values = (
            self._plot_action_category_unique_values(df=hist_data, category=category)
            if category is not None
            else (None, None)
        )

        if len(x_values) > 0:
            values = hist_data[feature]
            if feature not in self.cat_feature_names:
                if category is not None:
                    values = [
                        values[category_data == val] for val in category_unique_values
                    ]
                    hist_kwargs_.update(
                        color=clr[: len(category_unique_values)],
                        label=category_unique_values.astype(str),
                    )
                with warnings.catch_warnings():
                    warnings.filterwarnings(
                        "ignore", message="All-NaN slice encountered"
                    )
                    ax.hist(values, **hist_kwargs_)
                # sns.rugplot(data=chosen_data, height=0.05, ax=ax2, color='k')
                # ax2.set_ylim([0,1])
                if "range" not in hist_kwargs_.keys():
                    ax.set_xlim([np.min(x_values), np.max(x_values)])
                if kde:
                    self.plot_kde(
                        x_col=feature,
                        ax=ax,
                        **kde_kwargs_,
                    )
            else:
                counts = np.array(
                    [len(np.where(values.values == x)[0]) for x in x_values]
                )
                if category is not None:
                    bottom = np.zeros(len(x_values))
                    for idx, val in enumerate(category_unique_values):
                        category_counts = np.array(
                            [
                                len(
                                    np.where(values[category_data == val].values == x)[
                                        0
                                    ]
                                )
                                for x in x_values
                            ]
                        )
                        bar_kwargs_.update(
                            color=clr[idx], label=str(val), bottom=bottom
                        )
                        ax.bar(
                            x_values,
                            category_counts,
                            tick_label=[
                                self.cat_feature_mapping[feature][x] for x in x_values
                            ],
                            **bar_kwargs_,
                        )
                        bottom += category_counts
                else:
                    ax.bar(
                        x_values,
                        counts,
                        tick_label=[
                            self.cat_feature_mapping[feature][x] for x in x_values
                        ],
                        **bar_kwargs_,
                    )
                if "range" not in hist_kwargs_.keys():
                    ax.set_xlim([np.min(x_values) - 0.5, np.max(x_values) + 0.5])
                    count_range = np.max(counts) - np.min(counts)
                    ax.set_ylim(
                        [
                            max([np.min(counts) - 0.2 * count_range, 0]),
                            np.max(counts) + 0.2 * count_range,
                        ]
                    )
                plt.setp(
                    ax.get_xticklabels(),
                    rotation=90,
                    va="center",
                    ha="right",
                    rotation_mode="anchor",
                )
            if category is not None and legend:
                ax.legend(**legend_kwargs_)
        else:
            ax.text(0.5, 0.5, "Invalid interval", ha="center", va="center")
            ax.set_xlim([0, 1])
            ax.set_ylim([0, 1])
            ax.set_yticks([])

        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root, f"hist{'_imputed' if imputed else ''}_{feature}.pdf"
            ),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=feature,
            ylabel="Density" if hist_kwargs_["density"] else "Frequency",
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_on_one_axes(
        self,
        meth_name: Union[str, List],
        meth_kwargs_ls: List[Dict],
        twin: bool = False,
        fontsize: float = 12,
        xlabel: str = None,
        ylabel: str = None,
        twin_ylabel: str = None,
        ax=None,
        meth_fix_kwargs: Dict = None,
        figure_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
        legend: bool = False,
    ) -> matplotlib.axes.Axes:
        """
        Plot multiple items on one ``matplotlib.axes.Axes``.

        Parameters
        ----------
        meth_name
            The method or a list of methods to plot multiple items. The method should have an argument named `ax` which
            indicates the subplot.
        meth_kwargs_ls
            A list of arguments of the corresponding ``meth_name`` (except for ``ax``).
        twin
            Plot one plot on ``ax`` and the next plot on ``ax.twin()``.
        fontsize
            ``plt.rcParams["font.size"]``
        xlabel
            The overall xlabel.
        ylabel
            The overall ylabel.
        twin_ylabel
            The overall ylabel of the twin x-axis if ``twin`` is True.
        ax
            ``matplotlib.axes.Axes``
        meth_fix_kwargs
            Fixed arguments of ``meth_name`` (except for ``ax``, ``ls_kwarg_name``, and those given in
            ``meth_kwargs_ls``).
        figure_kwargs
            Arguments for ``plt.figure``.
        legend_kwargs
            Arguments for ``plt.legend()``
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.
        legend
            Whether to show the legend.

        Returns
        -------
        matplotlib.axes.Axes
        """
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        meth_fix_kwargs_ = update_defaults_by_kwargs(dict(), meth_fix_kwargs)

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        plt.rcParams["font.size"] = fontsize
        if isinstance(meth_name, str):
            meth_name = [meth_name] * len(meth_kwargs_ls)

        current_ax = ax
        twin_ax = ax.twinx() if twin else ax
        for meth, meth_kwargs in zip(meth_name, meth_kwargs_ls):
            getattr(self, meth)(ax=current_ax, **meth_kwargs, **meth_fix_kwargs_)
            current_ax = twin_ax if current_ax == ax and twin else ax

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        handlers, labels = ax.get_legend_handles_labels()
        if twin:
            twin_ax.set_ylabel(twin_ylabel)
            handlers_twin, labels_twin = twin_ax.get_legend_handles_labels()
            handlers += handlers_twin
            labels += labels_twin

        if legend:
            legend_kwargs_ = update_defaults_by_kwargs(
                dict(handles=handlers, labels=labels), legend_kwargs
            )
            ax.legend(**legend_kwargs_)

        return self._plot_action_after_plot(
            fig_name=os.path.join(self.project_root, "plot_on_one_axes.pdf"),
            disable=given_ax,
            ax_or_fig=ax,
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_scatter(
        self,
        x_col: str,
        y_col: str,
        category: str = None,
        ax=None,
        clr: Iterable = None,
        imputed: bool = False,
        kde_color: bool = False,
        figure_kwargs: Dict = None,
        scatter_kwargs: Dict = None,
        select_by_value_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot one column against another.

        Parameters
        ----------
        x_col
            The column for the x-axis.
        y_col
            The column for the y-axis.
        category
            The category to classify data points with different colors and markers.
        ax
            ``matplotlib.axes.Axes``
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        imputed
            Whether the imputed dataset should be considered.
        kde_color
            Whether the scatters are colored by their KDE density.
        figure_kwargs
            Arguments for ``plt.figure``.
        scatter_kwargs
            Arguments for ``plt.scatter()``
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        legend_kwargs
            Arguments for ``plt.legend``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        clr = global_palette if clr is None else clr
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        scatter_kwargs_ = update_defaults_by_kwargs(dict(color=clr[0]), scatter_kwargs)
        select_by_value_kwargs_ = update_defaults_by_kwargs(
            dict(), select_by_value_kwargs
        )
        legend_kwargs_ = update_defaults_by_kwargs(dict(), legend_kwargs)

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        df = self._plot_action_get_df(
            imputed=imputed, scaled=False, cat_transformed=False
        )
        indices = self.datamodule.select_by_value(**select_by_value_kwargs_)

        x = df.loc[indices, x_col].values.flatten()
        y = df.loc[indices, y_col].values.flatten()
        isna = np.union1d(np.where(np.isnan(x))[0], np.where(np.isnan(y))[0])
        notna = np.setdiff1d(np.arange(len(x)), isna)

        if kde_color:
            xy = np.vstack([x[notna], y[notna]])
            z = st.gaussian_kde(xy)(xy)
            idx = z.argsort()
            scatter_kwargs_ = update_defaults_by_kwargs(
                scatter_kwargs_, dict(c=z[idx], color=None)
            )
            ax.scatter(x[notna][idx], y[notna][idx], **scatter_kwargs_)
        else:
            if category is None:
                ax.scatter(x[notna], y[notna], **scatter_kwargs_)
            else:
                df = df.loc[indices, :].reset_index(drop=True)
                self._plot_action_categorical_scatter(
                    x=x[notna],
                    y=y[notna],
                    df=df.loc[notna, :],
                    category=category,
                    ax=ax,
                    clr=clr,
                    scatter_kwargs=scatter_kwargs_,
                )
                ax.legend(**legend_kwargs_)

        return self._plot_action_after_plot(
            fig_name=os.path.join(self.project_root, f"scatter_{x_col}_{y_col}.pdf"),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=x_col,
            ylabel=y_col,
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_pdf(
        self,
        feature: str,
        dist: st.rv_continuous = st.norm,
        ax=None,
        clr: Iterable = None,
        imputed: bool = False,
        figure_kwargs: Dict = None,
        plot_kwargs: Dict = None,
        select_by_value_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot the probability density function of a feature.

        Parameters
        ----------
        feature
            The investigated feature.
        dist
            The distribution to fit. It should be an instance of ``scipy.stats.rv_continuous`` that has ``fit`` and
            ``pdf`` methods.
        ax
            ``matplotlib.axes.Axes``
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        imputed
            Whether the imputed dataset should be considered.
        figure_kwargs
            Arguments for ``plt.figure``.
        plot_kwargs
            Arguments for ``plt.plot``
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        clr = global_palette if clr is None else clr
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        plot_kwargs_ = update_defaults_by_kwargs(dict(color=clr[0]), plot_kwargs)
        select_by_value_kwargs_ = update_defaults_by_kwargs(
            dict(), select_by_value_kwargs
        )

        df = self._plot_action_get_df(
            imputed=imputed, scaled=False, cat_transformed=False
        )
        indices = self.datamodule.select_by_value(**select_by_value_kwargs_)
        df = df.loc[indices, :]

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        values = df[feature].values.flatten()
        x = np.linspace(np.nanmin(values), np.nanmax(values), 200)
        pdf = dist.pdf(x, *dist.fit(values[np.isfinite(values)]))
        ax.plot(x, pdf, **plot_kwargs_)

        return self._plot_action_after_plot(
            fig_name=os.path.join(self.project_root, f"pdf_{feature}.pdf"),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=feature,
            ylabel="Probability density",
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_kde_all(
        self,
        imputed=False,
        fontsize=12,
        get_figsize_kwargs: Dict = None,
        figure_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
        tqdm_active: bool = False,
        **kwargs,
    ) -> matplotlib.figure.Figure:
        """
        Plot the kernel density estimation for each feature in the tabular data.

        Parameters
        ----------
        imputed
            Whether the imputed dataset should be considered.
        figure_kwargs
            Arguments for ``plt.figure``.
        fontsize
            ``plt.rcParams["font.size"]``
        get_figsize_kwargs
            Arguments for :func:`tabensemb.utils.utils.get_figsize`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure, or return the ``matplotlib.figure.Figure``
            instance.
        tqdm_active
            Whether to use a tqdm progress bar.
        **kwargs
            Arguments for :meth:`plot_kde`.

        Returns
        -------
        matplotlib.figure.Figure
            The figure if ``save_show_close`` is False.
        """
        savefig_kwargs_ = update_defaults_by_kwargs(
            dict(
                fname=os.path.join(
                    self.project_root, f"kdes{'_imputed' if imputed else ''}.pdf"
                )
            ),
            savefig_kwargs,
        )

        return self.plot_subplots(
            ls=self.cont_feature_names + self.label_name,
            ls_kwarg_name="x_col",
            meth_name="plot_kde",
            meth_fix_kwargs=dict(imputed=imputed, **kwargs),
            fontsize=fontsize,
            with_title=True,
            xlabel="Value of features",
            ylabel="Density",
            get_figsize_kwargs=get_figsize_kwargs,
            figure_kwargs=figure_kwargs,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs_,
            tqdm_active=tqdm_active,
        )

    def plot_kde(
        self,
        x_col: str,
        y_col: str = None,
        ax=None,
        clr: Iterable = None,
        imputed: bool = False,
        figure_kwargs: Dict = None,
        kdeplot_kwargs: Dict = None,
        select_by_value_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot the kernel density estimation of a feature or two features.

        Parameters
        ----------
        x_col
            The investigated feature.
        y_col
            If not None, a bi-variate distribution will be plotted.
        ax
            ``matplotlib.axes.Axes``
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        imputed
            Whether the imputed dataset should be considered.
        figure_kwargs
            Arguments for ``plt.figure``.
        kdeplot_kwargs
            Arguments for ``seaborn.kdeplot``
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        clr = global_palette if clr is None else clr
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        kdeplot_kwargs_ = update_defaults_by_kwargs(dict(color=clr[0]), kdeplot_kwargs)
        select_by_value_kwargs_ = update_defaults_by_kwargs(
            dict(), select_by_value_kwargs
        )

        df = self._plot_action_get_df(
            imputed=imputed, scaled=False, cat_transformed=False
        )
        indices = self.datamodule.select_by_value(**select_by_value_kwargs_)
        df = df.loc[indices, :]

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        sns.kdeplot(data=df, x=x_col, y=y_col, ax=ax, **kdeplot_kwargs_)
        ax.set_ylabel(None)
        ax.set_xlabel(None)

        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root,
                f"kde_{x_col}{'' if y_col is None else '_'+y_col}.pdf",
            ),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=x_col,
            ylabel="Density" if y_col is None else y_col,
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_presence_ratio(
        self,
        order="ratio",
        ax=None,
        clr: Iterable = None,
        figure_kwargs: Dict = None,
        barplot_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot the ratio of presence of each feature.

        Parameters
        ----------
        order
            "ratio" or "type". If is "ratio", the labels will be sorted by the presence ratio. If is "type", the labels
            will be sorted first by their feature types defined in the configuration, and then sorted by the presence
            ratio.
        ax
            ``matplotlib.axes.Axes``
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        figure_kwargs
            Arguments for ``plt.figure``.
        barplot_kwargs
            Arguments for ``seaborn.barplot``
        legend_kwargs
            Arguments for ``plt.legend``
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        barplot_kwargs_ = update_defaults_by_kwargs(
            dict(
                hue_order=self.datamodule.unique_feature_types_with_derived(),
                orient="h",
                linewidth=1,
                edgecolor="k",
                saturation=1,
            ),
            barplot_kwargs,
        )
        legend_kwargs_ = update_defaults_by_kwargs(
            dict(frameon=True, fancybox=True), legend_kwargs
        )
        is_horizontal = barplot_kwargs_["orient"] == "h"

        cont_mask = self.datamodule.cont_imputed_mask
        cat_mask = self.datamodule.cat_imputed_mask
        cont_presence_ratio = np.sum(1 - cont_mask) / cont_mask.shape[0]
        cat_presence_ratio = np.sum(1 - cat_mask) / cat_mask.shape[0]
        presence_ratio = pd.concat([cont_presence_ratio, cat_presence_ratio])
        presence = pd.DataFrame(
            {
                "feature": presence_ratio.index,
                "ratio": presence_ratio.values,
                "types": self.datamodule.get_feature_types(
                    list(presence_ratio.index), allow_unknown=True
                ),
            }
        )
        presence.sort_values(
            by=["types", "ratio"] if order == "type" else "ratio", inplace=True
        )

        clr = global_palette if clr is None else clr
        palette = self._plot_action_generate_feature_types_palette(
            clr=clr, features=presence["feature"]
        )

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        ax.set_axisbelow(True)
        ax.grid(axis="x", linewidth=0.2)
        sns.barplot(
            data=presence,
            x="ratio" if is_horizontal else "feature",
            y="feature" if is_horizontal else "ratio",
            ax=ax,
            palette=palette,
            **barplot_kwargs_,
        )
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        getattr(ax, "set_xlim" if is_horizontal else "set_ylim")([0, 1])

        legend = self._plot_action_generate_feature_types_legends(
            clr=clr, ax=ax, legend_kwargs=legend_kwargs_
        )

        return self._plot_action_after_plot(
            fig_name=os.path.join(self.project_root, f"presence_ratio.pdf"),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel="Presence ratio" if is_horizontal else "",
            ylabel="Presence ratio" if not is_horizontal else "",
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_fill_rating(
        self,
        ax=None,
        clr: Iterable = None,
        category: str = None,
        legend: bool = True,
        figure_kwargs: Dict = None,
        hist_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot the histogram of data point rating which is the percentage of filled features.

        Parameters
        ----------
        ax
            ``matplotlib.axes.Axes``
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        category
            The category to classify histograms and stack them with different colors.
        legend
            Show legends if ``category`` is not None.
        figure_kwargs
            Arguments for ``plt.figure``.
        hist_kwargs
            Arguments for ``plt.hist``.
        legend_kwargs
            Arguments for ``plt.legend`` if ``legend`` is True and ``category`` is not None.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes

        References
        ----------
        Zhang, Zian, and Zhiping Xu. “Fatigue Database of Additively Manufactured Alloys.” Scientific Data 10, no. 1 (May 2, 2023): 249.
        """
        clr = global_palette if clr is None else clr
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        hist_kwargs_ = update_defaults_by_kwargs(
            dict(linewidth=1, edgecolor="k", color=clr[0], density=True),
            hist_kwargs,
        )
        legend_kwargs_ = update_defaults_by_kwargs(dict(), legend_kwargs)

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        cont_mask = self.datamodule.cont_imputed_mask.values
        cat_mask = self.datamodule.cat_imputed_mask.values
        cont_presence_features = np.sum(1 - cont_mask, axis=1)
        cat_presence_features = np.sum(1 - cat_mask, axis=1)
        rating = (cont_presence_features + cat_presence_features) / len(
            self.all_feature_names
        )
        if category is not None:
            # augmented data points should not be included.
            df = self._plot_action_get_df(
                imputed=True, scaled=False, cat_transformed=False
            ).loc[self.datamodule.cont_imputed_mask.index, :]
            category_data, unique_values = self._plot_action_category_unique_values(
                df=df, category=category
            )
            rating = [rating[category_data == val] for val in unique_values]
            hist_kwargs_.update(
                dict(
                    label=unique_values.astype(str),
                    stacked=True,
                    color=clr[: len(unique_values)],
                )
            )
        ax.hist(rating, **hist_kwargs_)
        ax.set_xlim([0, 1])

        if legend and category is not None:
            ax.legend(**legend_kwargs_)

        return self._plot_action_after_plot(
            fig_name=os.path.join(self.project_root, f"fill_rating.pdf"),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel="Fill rating",
            ylabel="Density",
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_categorical_presence_ratio(
        self,
        category: str = None,
        ax=None,
        orient="h",
        figure_kwargs: Dict = None,
        imshow_kwargs: Dict = None,
        cbar_kwargs: Dict = None,
        cbar_ax_linewidth: float = 1,
        cbar_ax_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot the ratio of presence of each feature, but is classified by a categorical variable.

        Parameters
        ----------
        category
            The category (usually data sources) to classify data points.
        ax
            ``matplotlib.axes.Axes``
        figure_kwargs
            Arguments for ``plt.figure``.
        imshow_kwargs
            Arguments for ``plt.imshow``.
        cbar_kwargs
            Arguments for ``plt.colorbar``.
        cbar_ax_linewidth
            Line width of bounding box of cbar.
        cbar_ax_kwargs
            Arguments for ``mpl_toolkits.axes_grid1.inset_locator.inset_axes``
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        imshow_kwargs_ = update_defaults_by_kwargs(dict(cmap="Blues"), imshow_kwargs)
        cbar_kwargs_ = update_defaults_by_kwargs(dict(), cbar_kwargs)

        cont_mask = self.datamodule.cont_imputed_mask
        cat_mask = self.datamodule.cat_imputed_mask

        df = self._plot_action_get_df(
            imputed=False, scaled=False, cat_transformed=False
        ).loc[cont_mask.index, :]
        category_data, unique_values = self._plot_action_category_unique_values(
            df=df, category=category
        )

        mat = np.zeros((len(self.all_feature_names), len(unique_values)))
        for idx, cls in enumerate(unique_values):
            cls_indices = df.index[category_data == cls]
            cont_presence_ratio = np.sum(1 - cont_mask.loc[cls_indices, :]) / len(
                cls_indices
            )
            cat_presence_ratio = np.sum(1 - cat_mask.loc[cls_indices, :]) / len(
                cls_indices
            )
            presence_ratio = pd.concat([cont_presence_ratio, cat_presence_ratio])
            mat[:, idx] = presence_ratio[self.all_feature_names]

        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)
        im = ax.imshow(mat if orient == "h" else mat.T, **imshow_kwargs_)

        (ax.set_xticks if orient == "h" else ax.set_yticks)(
            np.arange(len(unique_values))
        )
        (ax.set_yticks if orient == "h" else ax.set_xticks)(
            np.arange(len(self.all_feature_names))
        )

        (ax.set_xticklabels if orient == "h" else ax.set_yticklabels)(unique_values)
        (ax.set_yticklabels if orient == "h" else ax.set_xticklabels)(
            self.all_feature_names
        )

        plt.setp(
            ax.get_xticklabels(),
            rotation=45,
            ha="right",
            va="center",
            rotation_mode="anchor",
        )

        from mpl_toolkits.axes_grid1.inset_locator import inset_axes

        cbar_ax_kwargs_ = update_defaults_by_kwargs(
            dict(
                width=f"{1/len(unique_values)*100}%",
                height="20%",
                loc="lower left",
                bbox_to_anchor=(1.05, 0.0, 1, 1),
                bbox_transform=ax.transAxes,
                borderpad=0,
            ),
            cbar_ax_kwargs,
        )
        axins = inset_axes(ax, **cbar_ax_kwargs_)

        cbar = ax.figure.colorbar(im, cax=axins, **cbar_kwargs_)
        cbar.ax.set_ylabel("Presence ratio", rotation=-90, va="bottom")
        [i.set_linewidth(cbar_ax_linewidth) for i in cbar.ax.spines.values()]
        cbar.ax.xaxis.set_tick_params(width=cbar_ax_linewidth)
        cbar.ax.yaxis.set_tick_params(width=cbar_ax_linewidth)

        return self._plot_action_after_plot(
            fig_name=os.path.join(self.project_root, f"presence_ratio_{category}.pdf"),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel=None,
            ylabel=None,
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def plot_pca_2d_visual(
        self,
        ax=None,
        category: str = None,
        clr: Iterable = None,
        features: List[str] = None,
        pca_kwargs: Dict = None,
        figure_kwargs: Dict = None,
        scatter_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        select_by_value_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Fit a ``sklearn.decomposition.PCA`` on a set of features, and plot its first two principal components as
        scatters.

        Parameters
        ----------
        ax
            ``matplotlib.axes.Axes``
        category
            The category to classify data points with different colors and markers.
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        features
            A subset of continuous features to fit the PCA.
        pca_kwargs
            Arguments for ``sklearn.decomposition.PCA.fit``
        figure_kwargs
            Arguments for ``plt.figure``.
        scatter_kwargs
            Arguments for ``plt.scatter``
        legend_kwargs
            Arguments for ``plt.legend``
        savefig_kwargs
            Arguments for ``plt.savefig``
        select_by_value_kwargs
            Arguments for :meth:`tabensemb.data.datamodule.DataModule.select_by_value`.
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        clr = global_palette if clr is None else clr
        features = self.cont_feature_names if features is None else features
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        pca_kwargs_ = update_defaults_by_kwargs(dict(random_state=0), pca_kwargs)
        scatter_kwargs_ = update_defaults_by_kwargs(dict(color=clr[0]), scatter_kwargs)
        legend_kwargs_ = update_defaults_by_kwargs(dict(title=category), legend_kwargs)
        select_by_value_kwargs_ = update_defaults_by_kwargs(
            dict(), select_by_value_kwargs
        )
        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        indices = self.datamodule.select_by_value(**select_by_value_kwargs_)
        df = (
            self._plot_action_get_df(imputed=True, scaled=True, cat_transformed=False)
            .loc[indices, :]
            .reset_index(drop=True)
        )
        pca = self.datamodule.pca(
            feature_names=features, indices=indices, **pca_kwargs_
        )
        low_dim_rep = pca.transform(df[features])
        x, y = low_dim_rep[:, 0], low_dim_rep[:, 1]

        if category is None:
            ax.scatter(x, y, **scatter_kwargs_)
        else:
            self._plot_action_categorical_scatter(
                x=x,
                y=y,
                df=df,
                category=category,
                ax=ax,
                clr=clr,
                scatter_kwargs=scatter_kwargs_,
            )
            ax.legend(**legend_kwargs_)

        return self._plot_action_after_plot(
            fig_name=os.path.join(self.project_root, f"pca_2d_visual_{category}.pdf"),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel="1st principal component",
            ylabel="2nd principal component",
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def _plot_action_category_unique_values(
        self, df: pd.DataFrame, category: str
    ) -> Tuple[pd.Series, np.ndarray]:
        """
        Get the category to classify data points and its unique values.

        Parameters
        ----------
        df
            The dataframe. The returned Series has the same indices.
        category
            The category to classify data points.

        Returns
        -------
        pd.Series
            The category
        np.ndarray
            Unique values.
        """
        df = self.datamodule.categories_inverse_transform(df)
        # Same as the procedure in OrdinalEncoder.
        dtype = get_imputed_dtype(df.dtypes[category])
        category_data = (
            fill_cat_nan(df[[category]], {category: dtype})[category]
            if dtype == str
            else df[category]
        )

        unique_values = np.sort(np.unique(category_data))
        return category_data, unique_values

    def _plot_action_categorical_scatter(
        self,
        x,
        y,
        df: pd.DataFrame,
        category: str,
        ax,
        clr: Iterable,
        scatter_kwargs: Dict,
    ):
        """
        Plot scatters whose colors are related to their category.

        Parameters
        ----------
        x
            x-values of the scatter plot.
        y
            y-values of the scatter plot.
        df
            The dataframe whose ``category`` column is used to classify data points.
        category
            The column to classify data points.
        ax
            ``matplotlib.axes.Axes``
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        scatter_kwargs
            Arguments for ``plt.scatter``
        """
        df = self.datamodule.categories_inverse_transform(df).reset_index(drop=True)
        category_data, unique_values = self._plot_action_category_unique_values(
            df=df, category=category
        )
        for idx, cat in enumerate(unique_values):
            colored_scatter_kwargs_ = scatter_kwargs.copy()
            colored_scatter_kwargs_.update(
                {
                    "color": clr[idx % len(clr)],
                    "marker": global_marker[idx % len(global_marker)],
                }
            )
            cat_indices = np.array(df[category_data == cat].index)
            ax.scatter(
                x[cat_indices],
                y[cat_indices],
                label=str(cat),
                **colored_scatter_kwargs_,
            )

    def plot_loss(
        self,
        program: str,
        model_name: str,
        ax=None,
        train_val: str = "both",
        restored_epoch_mark: bool = True,
        restored_epoch_mark_if_last: bool = False,
        legend: bool = True,
        clr: Iterable = None,
        plot_kwargs: Dict = None,
        scatter_kwargs: Dict = None,
        legend_kwargs: Dict = None,
        figure_kwargs: Dict = None,
        savefig_kwargs: Dict = None,
        save_show_close: bool = True,
    ) -> matplotlib.axes.Axes:
        """
        Plot loss curves for a model.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        ax
            ``matplotlib.axes.Axes``
        train_val
            "train" to plot training loss only. "val" to plot validation loss only. "both" to plot both of them.
        restored_epoch_mark
            Plot the best epoch from where the model is restored after training.
        restored_epoch_mark_if_last
            Plot the best epoch when it is the last epoch.
        legend
            Show legends.
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        plot_kwargs
            Arguments for ``plt.plot``
        scatter_kwargs
            Arguments for ``plt.scatter`` (used to plot the restored epoch).
        legend_kwargs
            Arguments for ``plt.legend``.
        figure_kwargs
            Arguments for ``plt.figure``.
        savefig_kwargs
            Arguments for ``plt.savefig``
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.

        Returns
        -------
        matplotlib.axes.Axes
        """
        clr = global_palette if clr is None else clr
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        plot_kwargs_ = update_defaults_by_kwargs(dict(markersize=4), plot_kwargs)
        scatter_kwargs_ = update_defaults_by_kwargs(
            dict(
                color=clr[2],
                marker=global_marker[2],
                s=15,
                label="Best epoch",
                zorder=10,
            ),
            scatter_kwargs,
        )
        legend_kwargs_ = update_defaults_by_kwargs(dict(), legend_kwargs)
        ax, given_ax = self._plot_action_init_ax(ax, figure_kwargs_)

        modelbase = self.get_modelbase(program=program)
        train_ls = modelbase.train_losses.get(model_name, None)
        val_ls = modelbase.val_losses.get(model_name, None)
        restored_epoch = modelbase.restored_epochs.get(model_name, None)

        if train_ls is None and val_ls is None:
            raise Exception(
                f"The model base {program} did not record losses during training in its attributes `train_losses` or "
                f"`val_losses` (in the `_train_single_model` method). "
            )

        if restored_epoch is None and restored_epoch_mark:
            warnings.warn(
                f"The model base {program} did not record the best epoch from where the model is restored in its "
                f"attribute `restored_epochs`  (in the `_train_single_model` method)"
            )

        if train_val in ["both", "train"] and train_ls is not None:
            train_plot_kwargs = plot_kwargs_.copy()
            train_plot_kwargs.update(
                dict(color=clr[0], marker=global_marker[0], label="Training loss")
            )
            ax.plot(np.arange(len(train_ls)), train_ls, **train_plot_kwargs)

        if train_val in ["both", "val"] and val_ls is not None:
            val_plot_kwargs = plot_kwargs_.copy()
            val_plot_kwargs.update(
                dict(color=clr[1], marker=global_marker[1], label="Validation loss")
            )
            ax.plot(np.arange(len(val_ls)), val_ls, **val_plot_kwargs)

        if (
            restored_epoch is not None
            and restored_epoch_mark
            and (restored_epoch < len(val_ls) - 1 or restored_epoch_mark_if_last)
        ):
            ax.scatter(
                restored_epoch,
                (val_ls if train_val in ["both", "val"] else train_ls)[restored_epoch],
                **scatter_kwargs_,
            )

        if legend:
            ax.legend(**legend_kwargs_)

        return self._plot_action_after_plot(
            fig_name=os.path.join(
                self.project_root, f"loss_{train_val}_{program}_{model_name}.pdf"
            ),
            disable=given_ax,
            ax_or_fig=ax,
            xlabel="Epoch",
            ylabel=f"{self.datamodule.loss.upper()} loss",
            tight_layout=False,
            save_show_close=save_show_close,
            savefig_kwargs=savefig_kwargs,
        )

    def _plot_action_generate_feature_types_palette(
        self, clr: Iterable, features: List[str]
    ) -> List:
        """
        Generate color palette for each feature according to their types defined in the configuration.

        Parameters
        ----------
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        features
            A list of features to be plotted.

        Returns
        -------
        list
            A list of colors for each feature. It can be used as the argument ``palette`` for seaborn functions.
        """
        type_idx = self.datamodule.get_feature_types_idx(
            features=features, allow_unknown=True
        )
        palette = [clr[i] for i in type_idx]
        return palette

    def _plot_action_generate_feature_types_legends(
        self, clr, ax, legend_kwargs
    ) -> matplotlib.legend.Legend:
        """
        Generate the legend for feature types defined in the configuration.

        Parameters
        ----------
        clr
            A seaborn color palette or an Iterable of colors. For example seaborn.color_palette("deep").
        ax
            ``matplotlib.axes.Axes``
        legend_kwargs
            Arguments for ``plt.legend``

        Returns
        -------
        matplotlib.legend.Legend
        """
        clr_map = dict()
        for idx, feature_type in enumerate(
            self.datamodule.unique_feature_types_with_derived()
        ):
            clr_map[feature_type] = clr[idx]
        legend_kwargs_ = update_defaults_by_kwargs(
            dict(
                loc="lower right",
                handleheight=2,
                fancybox=False,
                frameon=False,
            ),
            legend_kwargs,
        )

        legend = ax.legend(
            handles=[
                Rectangle((0, 0), 1, 1, color=value, ec="k", label=key)
                for key, value in clr_map.items()
            ],
            **legend_kwargs_,
        )

        return legend

    def _plot_action_init_ax(
        self, ax=None, figure_kwargs: Dict = None, return_fig: bool = False
    ) -> Tuple[matplotlib.axes.Axes, bool]:
        figure_kwargs_ = update_defaults_by_kwargs(dict(), figure_kwargs)
        given_ax = ax is not None
        if not given_ax:
            fig = plt.figure(**figure_kwargs_)
            if not return_fig:
                ax = plt.subplot(111)
        if isinstance(ax, matplotlib.axes.Axes):
            plt.sca(ax)
        return (ax, given_ax) if not return_fig else (fig, given_ax)

    def _plot_action_after_plot(
        self,
        fig_name,
        disable: bool,
        ax_or_fig=None,
        xlabel: str = None,
        ylabel: str = None,
        save_show_close: bool = True,
        tight_layout=False,
        savefig_kwargs: Dict = None,
    ) -> Union[matplotlib.axes.Axes, matplotlib.figure.Figure, Any]:
        """
        Set the labels of x/y-axis, set the layout, save the current figure, show the figure if in a notebook, and
        close the figure.

        Parameters
        ----------
        fig_name
            The path to save the figure. Can be updated by ``savefig_kwargs`` using the key ``fname``
        ax_or_fig
            ``matplotlib.axes.Axes`` or ``matplotlib.figure.Figure``. If is a ``matplotlib.axes.Axes``, x/y-axis labels
            will be set using ``xlabel`` and ``ylabel``.
        disable
            True to disable the action. ``ax_or_fig`` is still returned.
        xlabel
            The label of the x-axis. Will be set only when ``ax_or_fig`` is a ``matplotlib.axes.Axes``.
        ylabel
            The label of the y-axis. Will be set only when ``ax_or_fig`` is a ``matplotlib.axes.Axes``.
        save_show_close
            Whether to save, show (in the notebook), and close the figure if ``ax`` is not given.
        tight_layout
            If True, ``plt.tight_layout`` is called.
        savefig_kwargs
            Arguments for ``plt.savefig``.

        Returns
        -------
        matplotlib.axes.Axes or matplotlib.figure.Figure
            Just the input ``ax_or_fig``
        """
        if not disable:
            if ax_or_fig is not None:
                if isinstance(ax_or_fig, matplotlib.axes.Axes):
                    if xlabel is not None:
                        ax_or_fig.set_xlabel(xlabel)
                    if ylabel is not None:
                        ax_or_fig.set_ylabel(ylabel)
            if save_show_close:
                savefig_kwargs_ = update_defaults_by_kwargs(
                    dict(fname=fig_name), savefig_kwargs
                )
                if tight_layout:
                    plt.tight_layout()
                os.makedirs(os.path.dirname(savefig_kwargs_["fname"]), exist_ok=True)
                plt.savefig(**savefig_kwargs_)
                if is_notebook():
                    plt.show()
                plt.close()
        return ax_or_fig

    def _bootstrap_fit(
        self,
        program: str,
        df: pd.DataFrame,
        derived_data: Dict[str, np.ndarray],
        focus_feature: str,
        model_name: str,
        n_bootstrap: int = 1,
        grid_size: int = 30,
        refit: bool = True,
        resample: bool = True,
        percentile: float = 100,
        x_min: float = None,
        x_max: float = None,
        CI: float = 0.95,
        average: bool = True,
        inspect_attr_kwargs: Dict = None,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Make bootstrap resampling, fit the selected model on the resampled data, and assign sequential values to the
        selected feature to see how the prediction changes with respect to the feature.

        Cook, Thomas R., et al. Explaining Machine Learning by Bootstrapping Partial Dependence Functions and Shapley
        Values. No. RWP 21-12. 2021.

        Parameters
        ----------
        program
            The selected model base.
        model_name
            The selected model in the model base.
        df
            The tabular dataset.
        derived_data
            The derived data calculated using :meth:`derive_unstacked`.
        focus_feature
            The feature to assign sequential values.
        n_bootstrap
            The number of bootstrapping, fitting, and assigning runs.
        grid_size
            The number of sequential values.
        refit
            Whether to fit the model on the bootstrap dataset (with warm_start=True).
        resample
            Whether to do bootstrap resampling. Only recommended to False when n_bootstrap=1.
        percentile
            The percentile of the feature used to generate sequential values.
        x_min
            The lower limit of the generated sequential values. It will override the left percentile.
        x_max
            The upper limit of the generated sequential values. It will override the right percentile.
        CI
            The confidence interval level to evaluate bootstrapped predictions.
        average
            If True, CI will be calculated on results ``(grid_size, n_bootstrap)``where predictions for all samples are
            averaged for each bootstrap run.
            If False, CI will be calculated on results ``(grid_size, n_bootstrap*len(df))``.

        Returns
        -------
        np.ndarray
            The generated sequential values for the feature.
        np.ndarray
            Averaged predictions on the sequential values across multiple bootstrap runs and all samples.
        np.ndarray
            The left confidence interval.
        np.ndarray
            The right confidence interval.
        """
        from .utils import NoBayesOpt

        modelbase = self.get_modelbase(program)
        derived_data = self.datamodule.sort_derived_data(derived_data)
        df = df.reset_index(drop=True)
        if focus_feature in self.cont_feature_names:
            x_value = self._generate_grid(
                feature=focus_feature,
                grid_size=grid_size,
                percentile=percentile,
                x_min=x_min,
                x_max=x_max,
                df=df,
            )
        elif focus_feature in self.cat_feature_names:
            x_value = np.unique(df[focus_feature].values)
        else:
            raise Exception(f"{focus_feature} not available.")
        expected_value_bootstrap_replications = []
        inspects = []
        for i_bootstrap in range(n_bootstrap):
            if resample:
                df_bootstrap = skresample(df)
            else:
                df_bootstrap = df
            tmp_derived_data = self.datamodule.get_derived_data_slice(
                derived_data, list(df_bootstrap.index)
            )
            df_bootstrap = df_bootstrap.reset_index(drop=True)
            bootstrap_model = modelbase.detach_model(model_name=model_name)
            if refit:
                with NoBayesOpt(self):
                    bootstrap_model.fit(
                        df_bootstrap,
                        model_subset=[model_name],
                        cont_feature_names=self.datamodule.dataprocessors[
                            0
                        ].record_cont_features,
                        cat_feature_names=self.datamodule.dataprocessors[
                            0
                        ].record_cat_features,
                        label_name=self.label_name,
                        verbose=False,
                        warm_start=True,
                    )
            i_inspect = []
            bootstrap_model_predictions = []
            for value in x_value:
                df_perm = df_bootstrap.copy()
                df_perm[focus_feature] = value
                inspect_attr_kwargs_ = update_defaults_by_kwargs(
                    dict(attributes=[]), inspect_attr_kwargs
                )
                inspect = bootstrap_model.inspect_attr(
                    model_name=model_name,
                    df=df_perm,
                    derived_data=(
                        tmp_derived_data
                        if focus_feature in self.derived_stacked_features
                        else None
                    ),
                    **inspect_attr_kwargs_,
                )
                bootstrap_model_predictions.append(inspect["USER_INPUT"]["prediction"])
                i_inspect.append((value, inspect["USER_INPUT"]))
            if average:
                expected_value_bootstrap_replications.append(
                    np.mean(np.hstack(bootstrap_model_predictions), axis=0)
                )
            else:
                expected_value_bootstrap_replications.append(
                    np.hstack(bootstrap_model_predictions)
                )
            inspects.append(i_inspect)

        expected_value_bootstrap_replications = np.vstack(
            expected_value_bootstrap_replications
        )
        ci_left = []
        ci_right = []
        mean_pred = []
        for col_idx in range(expected_value_bootstrap_replications.shape[1]):
            y_pred = expected_value_bootstrap_replications[:, col_idx]
            if len(y_pred) != 1 and len(np.unique(y_pred)) != 1:
                ci_int = st.norm.interval(CI, loc=np.mean(y_pred), scale=np.std(y_pred))
            else:
                ci_int = (np.nan, np.nan)
            ci_left.append(ci_int[0])
            ci_right.append(ci_int[1])
            mean_pred.append(np.mean(y_pred))

        return (
            (x_value, np.array(mean_pred), np.array(ci_left), np.array(ci_right))
            if inspect_attr_kwargs is None
            else (
                x_value,
                np.array(mean_pred),
                np.array(ci_left),
                np.array(ci_right),
                inspects,
            )
        )

    def _generate_grid(
        self,
        feature: str,
        grid_size: int,
        percentile: Union[int, float] = 100,
        x_min: Union[int, float] = None,
        x_max: Union[int, float] = None,
        df: pd.DataFrame = None,
    ) -> np.ndarray:
        """
        Generate a sequential (linspace) grid for a feature in the tabular dataset.

        Parameters
        ----------
        feature
            The focused feature.
        grid_size
            The number of sequential values.
        percentile
            The percentile of the feature used to generate sequential values.
        x_min
            The lower limit of the generated sequential values. It will override the left percentile.
        x_max
            The upper limit of the generated sequential values. It will override the right percentile.
        df
            The tabular dataset.

        Returns
        -------
        np.ndarray
        """
        df = df if df is not None else self.df
        return np.linspace(
            (
                np.nanpercentile(df[feature].values, (100 - percentile) / 2)
                if x_min is None
                else x_min
            ),
            (
                np.nanpercentile(df[feature].values, 100 - (100 - percentile) / 2)
                if x_max is None
                else x_max
            ),
            grid_size,
        )

    def load_state(self, trainer: "Trainer"):
        """
        Restore a :class:`Trainer` from a deep-copied state.

        Parameters
        ----------
        trainer
            A deep-copied status of a :class:`Trainer`.
        """
        # https://stackoverflow.com/questions/1216356/is-it-safe-to-replace-a-self-object-by-another-object-of-the-same-type-in-a-meth
        current_root = cp(self.project_root)
        self.__dict__.update(trainer.__dict__)
        # The update operation does not change the location of self. However, model bases contains another trainer
        # that points to another location if the state is loaded from disk.
        for model in self.modelbases:
            model.trainer = self
        self.set_path(current_root, verbose=False)
        for modelbase in self.modelbases:
            modelbase.set_path(os.path.join(current_root, modelbase.program))

    def get_best_model(self) -> Tuple[str, str]:
        """
        Get the best model from :attr:`leaderboard`.

        Returns
        -------
        str
            The name of a model base where the best model is.
        model_name
            The name of the best model.
        """
        if not hasattr(self, "leaderboard"):
            self.get_leaderboard(test_data_only=True, dump_trainer=False)
        return (
            self.leaderboard["Program"].values[0],
            self.leaderboard["Model"].values[0],
        )

    def _metrics(
        self,
        predictions: Dict[str, Dict[str, Tuple[np.ndarray, np.ndarray]]],
        metrics: List[str],
        test_data_only: bool,
    ) -> pd.DataFrame:
        """
        Calculate metrics for predictions from :meth:`tabensemb.model.AbstractModel._predict_all`.

        Parameters
        ----------
        predictions
            Results from :meth:`tabensemb.model.AbstractModel._predict_all`.
        metrics
            The metrics that have been implemented in :func:`tabensemb.utils.utils.metric_sklearn`.
        test_data_only
            Whether to evaluate models only on testing datasets.

        Returns
        -------
        pd.DataFrame
            A dataframe of metrics.
        """
        df_metrics = pd.DataFrame()
        for model_name, model_predictions in predictions.items():
            df = pd.DataFrame(index=[0])
            df["Model"] = model_name
            for tvt, (y_pred, y_true) in model_predictions.items():
                if test_data_only and tvt != "Testing":
                    continue
                for metric in metrics:
                    metric_value = auto_metric_sklearn(
                        y_true, y_pred, metric, self.datamodule.task
                    )
                    df[
                        (
                            tvt + " " + metric.upper()
                            if not test_data_only
                            else metric.upper()
                        )
                    ] = metric_value
            df_metrics = pd.concat([df_metrics, df], axis=0, ignore_index=True)

        return df_metrics


def save_trainer(
    trainer: Trainer, path: Union[os.PathLike, str] = None, verbose: bool = True
):
    """
    Pickling the :class:`Trainer` instance.

    Parameters
    ----------
    trainer
        The :class:`Trainer` to be saved.
    path
        The folder path to save the :class:`Trainer`.
    verbose
        Verbosity.
    """
    import pickle

    path = os.path.join(trainer.project_root, "trainer.pkl") if path is None else path
    with open(path, "wb") as outp:
        pickle.dump(trainer, outp, pickle.HIGHEST_PROTOCOL)
    if verbose:
        print(
            f"Trainer saved. To load the trainer, run trainer = load_trainer(path='{path}')"
        )


def load_trainer(path: Union[os.PathLike, str]) -> Trainer:
    """
    Loading a pickled :class:`Trainer`. Paths of the :class:`Trainer` and its model bases (i.e. :attr:`project_root`,
    :attr:`tabensemb.model.AbstractModel.root`, :attr:`tabensemb.model.base.ModelDict.root`, and
    :meth:`tabensemb.model.base.ModelDict.model_path.keys`) will be changed.

    Parameters
    ----------
    path
        Path of the :class:`Trainer`.

    Returns
    -------
    trainer
        The loaded :class:`Trainer`.
    """
    import pickle

    with open(path, "rb") as inp:
        trainer = pickle.load(inp)
    root = os.path.join(*os.path.split(path)[:-1])
    trainer.set_path(root, verbose=False)
    for modelbase in trainer.modelbases:
        modelbase.set_path(os.path.join(root, modelbase.program))
        modelbase.trainer = trainer
    trainer.datamodule.args = trainer.args
    return trainer
