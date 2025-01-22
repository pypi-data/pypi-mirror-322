cfg = {
    "database": "sample",
    "task": None,
    "loss": None,
    "bayes_opt": False,
    "bayes_calls": 50,
    "bayes_epoch": 30,
    "patience": 100,
    "epoch": 300,
    "lr": 0.001,
    "weight_decay": 1e-9,
    "batch_size": 1024,
    "layers": [64, 128, 256, 128, 64],
    "SPACEs": {
        "lr": {
            "type": "Real",
            "low": 1e-4,
            "high": 0.05,
            "prior": "log-uniform",
        },
        "weight_decay": {
            "type": "Real",
            "low": 1e-9,
            "high": 0.05,
            "prior": "log-uniform",
        },
        "batch_size": {
            "type": "Categorical",
            "categories": [64, 128, 256, 512, 1024, 2048],
        },
    },
    "data_splitter": "RandomSplitter",
    "split_ratio": [0.6, 0.2, 0.2],
    "data_imputer": "MissForestImputer",
    "data_processors": [
        ("CategoricalOrdinalEncoder", {}),
        ("NaNFeatureRemover", {}),
        ("VarianceFeatureSelector", {"thres": 1}),
        ("StandardScaler", {}),
    ],
    "data_derivers": [],
    "categorical_feature_names": [],
    "continuous_feature_names": [],
    "feature_types": {},  # Will be automatically filled if not given.
    "unique_feature_types": [],  # Will be automatically over-written.
    "label_name": ["target"],
}
