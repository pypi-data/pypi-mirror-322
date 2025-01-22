import os
import pytest
from import_utils import *
import tabensemb
from tabensemb.config import UserConfig
from tabensemb.data import *
from tabensemb.data.dataderiver import RelativeDeriver, deriver_mapping
from tabensemb.data.dataimputer import get_data_imputer
from tabensemb.data.utils import OrdinalEncoder
from tabensemb.utils.utils import global_setting
import numpy as np
import pandas as pd
import torch
import copy

relative_deriver_kwargs = {
    "stacked": True,
    "absolute_col": "cont_0",
    "relative2_col": "cont_1",
    "intermediate": False,
    "derived_name": "derived_cont",
}
sample_weight_deriver_kwargs = {
    "stacked": True,
    "intermediate": True,
    "derived_name": "sample_weight",
}
categorical_deriver_kwargs = {
    "stacked": True,
    "intermediate": False,
    "derived_name": "derived_cat",
}


class DataCategoricalDeriver(AbstractDeriver):
    """
    This is an example of deriving categorical features.
    """

    def _required_cols(self):
        return []

    def _required_kwargs(self):
        return []

    def _defaults(self):
        return dict(stacked=True, intermediate=False, is_continuous=False)

    def _derived_names(self):
        return ["derived_cat_0", "derived_cat_1"]

    def _derive(self, df, datamodule):
        derived_cat_0 = df[["cat_1"]].values.flatten().reshape(-1, 1)
        derived_cat_1 = np.array(
            [f"category_{i}" for i in derived_cat_0.flatten()]
        ).reshape(-1, 1)
        return np.concatenate([derived_cat_0, derived_cat_1], axis=-1)


deriver_mapping["DataCategoricalDeriver"] = DataCategoricalDeriver


def pytest_configure_data():
    if getattr(pytest, "data_configure_excuted", False):
        return
    max_config = UserConfig("sample")
    processors = [
        ["CategoricalOrdinalEncoder", {}],
        ["NaNFeatureRemover", {}],
        ["VarianceFeatureSelector", {"thres": 0.1}],
        ["FeatureValueSelector", {"feature": "cat_1", "value": 0}],
        ["CorrFeatureSelector", {"thres": 0.1}],
        ["IQRRemover", {}],
        ["StdRemover", {}],
        ["SampleDataAugmenter", {}],
        ["StandardScaler", {}],
    ]
    relative_deriver_unstacked_kwargs = relative_deriver_kwargs.copy()
    relative_deriver_unstacked_kwargs["stacked"] = False
    relative_deriver_unstacked_kwargs["derived_name"] = "derived_cont_unstacked"
    derivers = [
        ("RelativeDeriver", relative_deriver_kwargs),
        ("RelativeDeriver", relative_deriver_unstacked_kwargs),
        ("SampleWeightDeriver", sample_weight_deriver_kwargs),
        ("DataCategoricalDeriver", categorical_deriver_kwargs),
        ("UnscaledDataDeriver", {"derived_name": "unscaled", "stacked": False}),
    ]
    max_config.merge({"data_processors": processors, "data_derivers": derivers})

    pytest.datamodule = DataModule(config=max_config)

    min_config = UserConfig("sample")
    min_config.merge({"data_derivers": derivers})
    pytest.min_datamodule = DataModule(config=min_config)

    np.random.seed(1)
    pytest.datamodule.load_data()
    pytest.min_datamodule.load_data()

    pytest.data_configure_excuted = True


@pytest.mark.order(1)
def test_load_data():
    pytest_configure_data()

    min_datamodule = pytest.min_datamodule
    dm = DataModule(min_datamodule.args)
    shuffled_index = np.array(min_datamodule.df.index)
    np.random.shuffle(shuffled_index)
    shuffled_df = min_datamodule.df.copy()
    shuffled_df.index = shuffled_index
    with pytest.raises(Exception) as err:
        dm.set_data(
            df=shuffled_df,
            cont_feature_names=min_datamodule.cont_feature_names,
            cat_feature_names=min_datamodule.cat_feature_names,
            label_name=min_datamodule.label_name,
        )
    assert "Call df.reset_index(drop=True)" in err.value.args[0]


def test_var_slip():
    pytest_configure_data()
    datamodule = pytest.datamodule
    assert np.allclose(
        datamodule.scaled_df.loc[datamodule.train_indices[0], "cont_0"],
        datamodule.get_var_change(
            "cont_0", datamodule.df.loc[datamodule.train_indices[0], "cont_0"]
        ),
    )
    datamodule.get_zero_slip("cont_0")


def test_split():
    pytest_configure_data()
    datamodule = pytest.datamodule
    AbstractSplitter._check_split(
        datamodule.train_indices,
        datamodule.val_indices,
        datamodule.test_indices,
    )


def test_augmentation():
    pytest_configure_data()
    datamodule = pytest.datamodule
    aug_desc = datamodule.df.loc[
        datamodule.augmented_indices - len(datamodule.dropped_indices),
        datamodule.all_feature_names + datamodule.label_name,
    ].describe()
    original_desc = datamodule.df.loc[
        datamodule.val_indices[-2:],
        datamodule.all_feature_names + datamodule.label_name,
    ].describe()
    assert np.allclose(
        aug_desc.values.astype(float), original_desc.values.astype(float)
    )
    AbstractSplitter._check_split(
        datamodule.train_indices, datamodule.val_indices, datamodule.test_indices
    )
    assert all(
        [
            x in datamodule.train_indices
            for x in datamodule.augmented_indices - len(datamodule.dropped_indices)
        ]
    )


def test_prepare_new_data_randpermed():
    pytest_configure_data()

    def test_one_datamodule(datamodule):
        df = datamodule.df.copy()
        indices = np.array(df.index)
        np.random.shuffle(indices)
        df.index = indices
        df, derived_data = datamodule.prepare_new_data(df)
        assert np.allclose(
            df[datamodule.all_feature_names + datamodule.label_name].values,
            datamodule.df[datamodule.all_feature_names + datamodule.label_name].values,
        ), "Stacked features from prepare_new_data for the set dataframe does not get consistent results"
        assert len(derived_data) == len(datamodule.derived_data), (
            "The number of unstacked features from "
            "prepare_new_data is not consistent"
        )
        for key, value in datamodule.derived_data.items():
            if key != "augmented":
                assert np.allclose(value, derived_data[key]), (
                    f"Unstacked feature `{key}` from prepare_new_data for the set "
                    "dataframe does not get consistent results"
                )

    test_one_datamodule(pytest.min_datamodule)
    test_one_datamodule(pytest.datamodule)


def test_prepare_new_data_categorical_label():
    pytest_configure_data()
    config = UserConfig.from_uci(
        "Iris", column_names=iris_columns, datafile_name="iris"
    )
    datamodule = DataModule(config=config)
    datamodule.load_data()
    csv_path = os.path.join(
        tabensemb.setting["default_data_path"], config["database"] + ".csv"
    )
    original_df = pd.read_csv(csv_path)
    os.remove(csv_path)
    df, derived_data = datamodule.prepare_new_data(original_df)
    assert np.equal(
        datamodule.df[datamodule.all_feature_names].values,
        df[datamodule.all_feature_names].values,
    ).all()
    assert np.equal(
        datamodule.df[datamodule.label_name].values, df[datamodule.label_name].values
    ).all()
    inv_df = datamodule.label_categories_inverse_transform(df)
    assert np.equal(
        original_df[datamodule.label_name].values, inv_df[datamodule.label_name].values
    ).all()


def test_prepare_new_data_absent():
    pytest_configure_data()
    datamodule = pytest.min_datamodule
    with pytest.raises(Exception) as err:
        datamodule.prepare_new_data(
            datamodule.df[datamodule.cont_feature_names[:2]], datamodule.derived_data
        )
    assert "not in the input dataframe" in err.value.args[0]

    test_derived_data = datamodule.derived_data.copy()
    del test_derived_data[list(test_derived_data.keys())[0]]
    with pytest.raises(Exception) as err:
        datamodule.prepare_new_data(datamodule.df, test_derived_data)
    assert "not in the input derived_data" in err.value.args[0]


@pytest.mark.order(before="test_set_feature_names")
def test_data_deriver():
    pytest_configure_data()
    datamodule = pytest.min_datamodule
    assert "derived_cont" in datamodule.cont_feature_names
    assert "derived_cont_unstacked" not in datamodule.cont_feature_names
    assert "derived_cat_0" in datamodule.cat_feature_names
    assert "derived_cat_1" in datamodule.cat_feature_names
    assert "derived_cont_unstacked" in datamodule.derived_data.keys()
    assert "sample_weight" in datamodule.df.columns
    assert "sample_weight" not in datamodule.cont_feature_names


@pytest.mark.order(before="test_set_feature_names")
def test_describe():
    pytest_configure_data()
    datamodule = pytest.min_datamodule
    datamodule.describe()
    datamodule.cal_corr()


@pytest.mark.order(before="test_set_feature_names")
def test_get_not_imputed():
    pytest_configure_data()
    not_imputed = pytest.datamodule.get_not_imputed_df()
    cont_mask = pytest.datamodule.cont_imputed_mask
    cont_missing = np.where(cont_mask.values == 1)
    assert all(
        [
            np.isnan(not_imputed.values[cont_missing[0][i], cont_missing[1][i]])
            for i in range(len(cont_missing[0]))
        ]
    )

    cat_mask = pytest.datamodule.cat_imputed_mask
    cat_missing = np.where(cat_mask.values == 1)
    assert all(
        [
            np.isnan(not_imputed.values[cat_missing[0][i], cat_missing[1][i]])
            for i in range(len(cat_missing[0]))
        ]
    )


@pytest.mark.order(before="test_set_feature_names")
def test_get_feature_by_type():
    pytest_configure_data()
    datamodule = pytest.datamodule
    cont = datamodule.get_feature_names_by_type("Continuous")
    cont_idx = datamodule.get_feature_idx_by_type("Continuous", var_type="continuous")
    assert all(
        [
            got in datamodule.cont_feature_names
            and got not in datamodule.get_all_derived_stacked_feature_names()
            for got in cont
        ]
    )
    assert all(
        [
            datamodule.cont_feature_names.index(name) == idx
            for name, idx in zip(cont, cont_idx)
        ]
    )
    cat = datamodule.get_feature_names_by_type("Categorical")
    cat_idx = datamodule.get_feature_idx_by_type("Categorical", var_type="categorical")
    assert all([real == got for real, got in zip(datamodule.cat_feature_names, cat)])
    assert all(
        [
            real == got
            for real, got in zip(range(len(datamodule.cat_feature_names)), cat_idx)
        ]
    )
    with pytest.raises(Exception) as err:
        datamodule.get_feature_names_by_type("TEST")
    assert "invalid" in err.value.args[0]


@pytest.mark.order(before="test_set_feature_names")
def test_get_feature_types():
    pytest_configure_data()
    datamodule = pytest.datamodule
    types = datamodule.get_feature_types(
        [
            datamodule.cont_feature_names[0],
            datamodule.cat_feature_names[0],
            "derived_cont",
            "derived_cont_unstacked",
            "derived_cat_0",
        ],
        allow_unknown=True,
    )
    assert (
        "derived_cont" not in datamodule.cont_feature_names
    )  # Removed by CorrFeatureSelector
    assert (
        "Continuous" == types[0]
        and "Categorical" == types[1]
        and "Unknown" == types[2]
        and "Unknown" == types[3]
        and "Derived" == types[4]
    )

    idxs = datamodule.get_feature_types_idx(
        [
            datamodule.cont_feature_names[0],
            datamodule.cat_feature_names[0],
            "derived_cont",
            "derived_cont_unstacked",
            "derived_cat_0",
        ],
        allow_unknown=True,
    )
    assert (
        idxs[0] == datamodule.unique_feature_types_with_derived().index("Continuous")
        and idxs[1]
        == datamodule.unique_feature_types_with_derived().index("Categorical")
        and idxs[2] == 3
        and idxs[3] == 3
        and idxs[4] == datamodule.unique_feature_types_with_derived().index("Derived")
    )

    with pytest.raises(Exception) as err:
        datamodule.get_feature_types(
            ["TEST", datamodule.cont_feature_names[0], datamodule.cat_feature_names[0]],
            allow_unknown=False,
        )
    assert (
        "TEST" in err.value.args[0]
        and datamodule.cont_feature_names[0] not in err.value.args[0]
        and datamodule.cat_feature_names[0] not in err.value.args[0]
    )

    types = datamodule.get_feature_types(
        ["TEST"],
        allow_unknown=True,
    )
    assert "Unknown" == types[0]


@pytest.mark.order(before="test_set_feature_names")
def test_extract_names():
    pytest_configure_data()
    datamodule = pytest.datamodule
    names = [datamodule.cont_feature_names[0], datamodule.cat_feature_names[0]]

    assert len(datamodule.extract_derived_stacked_feature_names(names)) == 0

    with_derived = datamodule.extract_derived_stacked_feature_names(
        ["derived_cont", "derived_cont_unstacked", "derived_cat_0"] + names
    )
    assert (
        len(with_derived) == 2
        and "derived_cont" in with_derived
        and "derived_cat_0" in with_derived
    )

    extract_cont = datamodule.extract_original_cont_feature_names(
        ["derived_cont", "derived_cont_unstacked", "derived_cat_0"] + names
    )
    assert len(extract_cont) == 1 and datamodule.cont_feature_names[0] in extract_cont

    extract_cat = datamodule.extract_original_cat_feature_names(
        ["derived_cont", "derived_cont_unstacked", "derived_cat_0"] + names
    )
    assert len(extract_cat) == 1 and datamodule.cat_feature_names[0] in extract_cat

    all_stacked = datamodule.get_all_derived_stacked_feature_names()
    assert (
        len(all_stacked) == 3
        and "derived_cont" in all_stacked
        and "derived_cat_0" in all_stacked
        and "derived_cat_1" in all_stacked
    )


def test_set_feature_names():
    pytest_configure_data()
    datamodule = pytest.datamodule

    # set without continuous features
    no_cont_datamodule = copy.deepcopy(datamodule)
    no_cont_datamodule.set_feature_names(datamodule.cat_feature_names)
    assert len(no_cont_datamodule.cont_feature_names) == 0

    # set without categorical features
    no_cat_datamodule = copy.deepcopy(datamodule)
    no_cat_datamodule.set_feature_names(datamodule.cont_feature_names)
    assert len(no_cat_datamodule.cat_feature_names) == 0

    # Prepare new data after set feature names

    def test_one_datamodule(datamodule, expected_cont, expected_cat):
        df, derived_data = datamodule.prepare_new_data(datamodule.df)
        assert (
            len(datamodule.cont_feature_names) == expected_cont
            and len(datamodule.cat_feature_names) == expected_cat
            and len(datamodule.label_name) == 1
        ), "set_feature_names is not functional when prepare_new_data."
        assert np.allclose(
            df[datamodule.all_feature_names + datamodule.label_name].values,
            datamodule.df[datamodule.all_feature_names + datamodule.label_name].values,
        ), (
            "Stacked features from prepare_new_data after set_feature_names for the set dataframe does not get "
            "consistent results"
        )
        assert len(derived_data) == len(datamodule.derived_data), (
            "The number of unstacked features after set_feature_names from "
            "prepare_new_data is not consistent"
        )
        for key, value in datamodule.derived_data.items():
            if key != "augmented":
                assert np.allclose(value, derived_data[key]), (
                    f"Unstacked feature `{key}` after set_feature_names from prepare_new_data for the set "
                    "dataframe does not get consistent results"
                )

    no_cont_datamodule = copy.deepcopy(datamodule)
    no_cont_datamodule.set_feature_names(
        datamodule.cat_feature_names[:1] + ["derived_cat_0"]
    )
    test_one_datamodule(no_cont_datamodule, expected_cont=0, expected_cat=2)

    no_cat_datamodule = copy.deepcopy(datamodule)
    no_cat_datamodule.set_feature_names(datamodule.cont_feature_names[:2])
    test_one_datamodule(no_cat_datamodule, expected_cont=2, expected_cat=0)

    # Remove feature
    df = no_cat_datamodule.df.copy()
    original_cont_names = no_cat_datamodule.cont_feature_names.copy()
    df[no_cat_datamodule.cont_feature_names[0]] = 1.0
    no_cat_datamodule.set_data(
        no_cat_datamodule.categories_inverse_transform(df),
        cont_feature_names=no_cat_datamodule.cont_feature_names,
        cat_feature_names=no_cat_datamodule.cat_feature_names,
        label_name=no_cat_datamodule.label_name,
    )
    new_cont_names = no_cat_datamodule.cont_feature_names.copy()

    # "cont_0" is removed and "derived_cont" is added back.
    assert len(original_cont_names) == len(new_cont_names)
    assert (
        original_cont_names[0] not in new_cont_names
        and "derived_cont" in new_cont_names
    )


def test_sort_derived_data():
    pytest_configure_data()
    datamodule = pytest.min_datamodule

    derived_data = datamodule.derived_data
    reversed_derived_data = {
        key: derived_data[key] for key in list(derived_data.keys())[::-1]
    }
    sorted_derived_data = datamodule.sort_derived_data(reversed_derived_data)
    assert all(
        [
            key1 == key2
            for key1, key2 in zip(derived_data.keys(), sorted_derived_data.keys())
        ]
    )
    absent_derived_data = derived_data.copy()
    del absent_derived_data[list(derived_data.keys())[0]]
    with pytest.raises(KeyError):
        datamodule.sort_derived_data(absent_derived_data)
    datamodule.sort_derived_data(absent_derived_data, ignore_absence=True)


def test_categorical_transform():
    pytest_configure_data()
    datamodule = pytest.min_datamodule

    test_df = datamodule.df[datamodule.cat_feature_names]
    returned = datamodule.categories_inverse_transform(test_df)
    assert (
        returned.loc[0, "derived_cat_1"]
        == datamodule.cat_feature_mapping["derived_cat_1"][
            test_df.loc[0, "derived_cat_1"]
        ]
    )
    assert np.all(np.equal(test_df[["cat_1"]].values, returned[["cat_1"]].values))
    # "cat_2" has unknown values, which is first filled with -1 and will be encoded as 0.
    assert np.all(np.equal(test_df[["cat_2"]].values, returned[["cat_2"]].values + 1))

    return_inversed = datamodule.categories_inverse_transform(
        test_df[["derived_cat_1"]]
    )
    assert (
        return_inversed.loc[0, "derived_cat_1"]
        == datamodule.cat_feature_mapping["derived_cat_1"][
            test_df.loc[0, "derived_cat_1"]
        ]
    )

    return_encoded = datamodule.categories_transform(return_inversed)
    assert np.all(np.equal(test_df[["derived_cat_1"]].values, return_encoded.values))

    returned_same = datamodule.categories_inverse_transform(returned[["derived_cat_1"]])
    assert all([x == y for x, y in zip(returned_same, returned[["derived_cat_1"]])])

    permuted_df = test_df.copy()
    permuted_df.index = np.random.permutation(test_df.index)
    return_same_index = datamodule.categories_inverse_transform(permuted_df)
    assert all([x == y for x, y in zip(permuted_df.index, return_same_index.index)])


def test_ordinal_encoder():
    df = pd.DataFrame(
        {"col1": [1, 2, np.nan, 4], "col2": ["cat_1", "cat_2", 3, np.nan]}
    )
    df_test = pd.DataFrame(
        {
            "col1": [1, 2, np.nan, 4, 5],
            "col2": ["cat_1", "cat_2", 3, np.nan, "cat_4"],
        }
    )
    oe = OrdinalEncoder()
    oe.fit(df)
    res_trans = oe.transform(df_test)
    assert np.issubdtype(res_trans.values.dtype, int)
    # assert res_trans.loc[2, "col1"] == tabensemb.data.utils.number_unknown_value
    # assert res_trans.loc[3, "col2"] == tabensemb.data.utils.object_unknown_value
    assert len(np.unique(res_trans["col1"])) == 4
    assert len(np.unique(res_trans["col2"])) == 4

    res_inv_trans = oe.inverse_transform(res_trans)
    assert res_inv_trans.loc[0, "col1"] == 1
    assert res_inv_trans.loc[1, "col1"] == 2
    assert res_inv_trans.loc[2, "col1"] == tabensemb.data.utils.number_unknown_value
    assert res_inv_trans.loc[3, "col1"] == 4
    assert res_inv_trans.loc[4, "col1"] == tabensemb.data.utils.number_unknown_value

    assert res_inv_trans.loc[0, "col2"] == "cat_1"
    assert res_inv_trans.loc[1, "col2"] == "cat_2"
    assert res_inv_trans.loc[2, "col2"] == "3"
    assert res_inv_trans.loc[3, "col2"] == tabensemb.data.utils.object_unknown_value
    assert res_inv_trans.loc[4, "col2"] == tabensemb.data.utils.object_unknown_value

    res_inv_trans_same = oe.inverse_transform(df_test)
    assert len(res_inv_trans_same.columns) == 2
    assert res_inv_trans_same.loc[0, "col1"] == 1
    assert res_inv_trans_same.loc[1, "col1"] == 2
    assert np.isnan(res_inv_trans_same.loc[2, "col1"])
    assert res_inv_trans_same.loc[3, "col1"] == 4
    assert res_inv_trans_same.loc[4, "col1"] == 5

    res_inv_trans_same = oe.inverse_transform(df_test[["col2"]])
    assert len(res_inv_trans_same.columns) == 1
    assert res_inv_trans_same.loc[0, "col2"] == "cat_1"
    assert res_inv_trans_same.loc[1, "col2"] == "cat_2"
    assert res_inv_trans_same.loc[2, "col2"] == 3
    assert np.isnan(res_inv_trans_same.loc[3, "col2"])
    assert res_inv_trans_same.loc[4, "col2"] == "cat_4"

    df_test_not_int = pd.DataFrame(
        {
            "col1": [1, 2, 1.1, np.nan],
        }
    )
    with pytest.raises(Exception) as err:
        oe.inverse_transform(df_test_not_int)
    assert "is not integeral" in err.value.args[0]

    df_all_int = pd.DataFrame({"col1": [1, 2, 4, np.nan]})
    res_all_int = oe.transform(df_all_int)
    assert (
        res_all_int.loc[0, "col1"] != 1
        or res_all_int.loc[1, "col1"] != 2
        or res_all_int.loc[2, "col1"] != 4
    )
    res_inv_all_int = oe.inverse_transform(df_all_int)
    assert (
        res_inv_all_int.loc[0, "col1"] != 1
        or res_inv_all_int.loc[1, "col1"] != 2
        or res_inv_all_int.loc[2, "col1"] == -1
    )


def test_base_predictor():
    pytest_configure_data()
    datamodule = pytest.min_datamodule
    predictor = datamodule.get_base_predictor(categorical=True, n_estimators=2)
    predictor.fit(
        datamodule.df[datamodule.all_feature_names],
        datamodule.label_data.values.flatten(),
    )

    predictor = datamodule.get_base_predictor(categorical=False, n_estimators=2)
    predictor.fit(
        datamodule.df[datamodule.all_feature_names],
        datamodule.label_data.values.flatten(),
    )


def test_rfe():
    config = UserConfig("sample")
    min_features_to_select = 3
    config.merge(
        {
            "data_processors": [
                ["CategoricalOrdinalEncoder", {}],
                ["NaNFeatureRemover", {}],
                ["VarianceFeatureSelector", {"thres": 1}],
                [
                    "RFEFeatureSelector",
                    {
                        "n_estimators": 2,
                        "min_features_to_select": min_features_to_select,
                        "verbose": 1,
                        "method": "shap",
                    },
                ],
                ["StandardScaler", {}],
            ],
        }
    )

    print("\n-- Loading datamodule --\n")
    datamodule = DataModule(config=config)

    print("\n-- Loading data --\n")
    np.random.seed(1)
    datamodule.load_data()

    assert len(datamodule.cont_feature_names) >= min_features_to_select


def test_illegal_cont_feature():
    config = UserConfig("sample")
    # "cat_1" is not object
    config.merge(
        {
            "continuous_feature_names": ["cont_0"],
            "categorical_feature_names": ["cat_1"],
        }
    )
    datamodule = DataModule(config=config)
    datamodule.load_data()

    # "cat_0" is object and cannot be converted
    with pytest.raises(Exception) as err:
        datamodule.set_data(
            datamodule.categories_inverse_transform(datamodule.df),
            cont_feature_names=["cont_0", "cat_0"],
            cat_feature_names=[],
            label_name=datamodule.label_name,
        )
    assert "are object, but are included in continuous features" in err.value.args[0]

    df = datamodule.df.copy()
    df["cat_1"] = df["cat_1"].values.astype(object)
    datamodule.set_data(
        datamodule.categories_inverse_transform(df),
        cont_feature_names=["cont_0", "cat_1"],
        cat_feature_names=[],
        label_name=datamodule.label_name,
    )


def test_data_splitter():
    import numpy as np
    import pandas as pd
    from tabensemb.data.datasplitter import RandomSplitter

    df = pd.DataFrame({"test_feature": np.random.randint(0, 20, (100,))})
    print("\n-- k-fold RandomSplitter --\n")
    spl = RandomSplitter()
    res_random = [spl.split(df, [], [], [], cv=5) for i in range(5)]
    assert np.allclose(
        np.sort(np.hstack([i[2] for i in res_random])), np.arange(100)
    ), "RandomSplitter is not getting correct k-fold results."

    print("\n-- k-fold RandomSplitter in a new iteration --\n")
    with pytest.warns(UserWarning):
        res_random = [spl.split(df, [], [], [], cv=5) for i in range(5)]
    assert np.allclose(
        np.sort(np.hstack([i[2] for i in res_random])), np.arange(100)
    ), "RandomSplitter is not getting correct k-fold results in a new iteration."

    print("\n-- k-fold RandomSplitter change k --\n")
    with pytest.warns(UserWarning):
        spl.split(df, [], [], [], cv=5)
    with pytest.warns(UserWarning):
        res_random = [spl.split(df, [], [], [], cv=3) for i in range(3)]
    assert np.allclose(
        np.sort(np.hstack([i[2] for i in res_random])), np.arange(100)
    ), "RandomSplitter is not getting correct k-fold results after changing the number of k-fold."

    print("\n-- Non-cv RandomSplitter --\n")
    spl = RandomSplitter()
    res_random = [spl.split(df, [], [], []) for i in range(5)]
    res = np.sort(np.hstack([i[2] for i in res_random]))
    assert len(res) != 100 or (
        len(res) == 100 and not np.allclose(res, np.arange(100))
    ), "RandomSplitter is getting k-fold results without cv arguments."


def test_data_imputer():
    config = UserConfig("sample")
    config.merge({"data_derivers": [("RelativeDeriver", relative_deriver_kwargs)]})
    datamodule = DataModule(config=config)

    print("\n-- MeanImputer --\n")
    datamodule.set_data_imputer("MeanImputer")
    datamodule.load_data()
    assert not np.any(pd.isna(datamodule.df[datamodule.all_feature_names]).values)

    original = datamodule.get_not_imputed_df()

    print("\n-- MedianImputer --\n")
    imputer = get_data_imputer("MedianImputer")()
    imputed = imputer.fit_transform(original.copy(), datamodule)
    assert not np.any(pd.isna(imputed[datamodule.all_feature_names]).values)

    print("\n-- ModeImputer --\n")
    imputer = get_data_imputer("ModeImputer")()
    imputed = imputer.fit_transform(original.copy(), datamodule)
    assert not np.any(pd.isna(imputed[datamodule.all_feature_names]).values)

    print("\n-- MiceLightgbmImputer --\n")
    imputer = get_data_imputer("MiceLightgbmImputer")()
    imputed = imputer.fit_transform(original.copy(), datamodule)
    assert not np.any(pd.isna(imputed[datamodule.all_feature_names]).values)

    print("\n-- MiceImputer --\n")
    imputer = get_data_imputer("MiceImputer")(max_iter=10)
    imputed = imputer.fit_transform(original.copy(), datamodule)
    assert not np.any(pd.isna(imputed[datamodule.all_feature_names]).values)

    print("\n-- MissForestImputer --\n")
    imputer = get_data_imputer("MissForestImputer")()
    imputed = imputer.fit_transform(original.copy(), datamodule)
    assert not np.any(pd.isna(imputed[datamodule.all_feature_names]).values)

    print("\n-- GainImputer --\n")
    imputer = get_data_imputer("GainImputer")(n_epochs=10)
    imputed = imputer.fit_transform(original.copy(), datamodule)
    assert not np.any(pd.isna(imputed[datamodule.all_feature_names]).values)


def test_pca():
    config = UserConfig("sample")
    config.merge({"data_derivers": [("RelativeDeriver", relative_deriver_kwargs)]})
    datamodule = DataModule(config=config)
    datamodule.load_data()

    pca1 = datamodule.pca(feature_names=datamodule.cont_feature_names)
    pca2 = datamodule.pca(
        feature_idx=list(np.arange(len(datamodule.cont_feature_names)))
    )
    pca3 = datamodule.pca()
    pca4 = datamodule.pca(indices=datamodule.test_indices)

    assert np.allclose(pca1.components_, pca2.components_)
    assert np.allclose(pca1.components_, pca3.components_)
    assert not np.allclose(pca1.components_, pca4.components_)


def test_abstract_deriver():
    pytest_configure_data()
    datamodule = pytest.min_datamodule

    class NotImplementedDeriver(AbstractDeriver):
        def _required_cols(self):
            return []

    with pytest.raises(Exception) as err:
        # "stacked", "intermediate", "derived_name", and "is_continuous" is not specified.
        _ = NotImplementedDeriver()
    assert "stacked" in err.value.args[0]
    deriver = NotImplementedDeriver(
        **{
            "stacked": True,
            "intermediate": False,
            "derived_name": "TEST_DERIVED",
            "is_continuous": True,
        }
    )
    with pytest.raises(NotImplementedError):
        deriver._derive(datamodule.df, datamodule)
    with pytest.raises(NotImplementedError):
        super(NotImplementedDeriver, deriver)._required_cols()

    with pytest.raises(Exception) as err:
        _ = RelativeDeriver(**{"relative2_col": "TEST", "derived_name": "TEST_DERIVED"})
    assert "absolute_col" in err.value.args[0]
    legal_deriver = RelativeDeriver(
        **{
            "relative2_col": "TEST",
            "absolute_col": "TEST",
            "derived_name": "TEST_DERIVED",
        }
    )
    legal_deriver._check_arg(name="relative2_col")
    with pytest.raises(Exception) as err:
        legal_deriver._check_exist(df=datamodule.df, name="relative2_col")
    assert "is not a valid column" in err.value.args[0]
    legal_deriver.kwargs["relative2_col"] = "cont_0"
    legal_deriver._check_exist(df=datamodule.df, name="relative2_col")
    with pytest.raises(Exception) as err:
        legal_deriver._check_values(np.zeros((len(datamodule.df),)))
    assert "returns a one dimensional" in err.value.args[0]
    legal_deriver._check_values(np.zeros((len(datamodule.df), 1)))
    legal_deriver._check_values(np.zeros((len(datamodule.df), 2)))

    assert len(deriver._defaults()) == 0


def test_abstract_imputer():
    pytest_configure_data()
    datamodule = pytest.min_datamodule

    class NotImplementedImputer(AbstractImputer): ...

    imputer = NotImplementedImputer()
    with pytest.raises(NotImplementedError):
        imputer._fit_transform(datamodule.df, datamodule)
    with pytest.raises(NotImplementedError):
        imputer._transform(datamodule.df, datamodule)

    print("\n-- AbstractSklearnImputer--\n")

    class NotImplementedImputer(AbstractSklearnImputer): ...

    imputer = NotImplementedImputer()
    with pytest.raises(NotImplementedError):
        imputer._new_imputer()


def test_abstract_processor():
    pytest_configure_data()
    datamodule = pytest.min_datamodule

    class NotImplementedProcessor(AbstractProcessor): ...

    processor = NotImplementedProcessor()
    with pytest.raises(NotImplementedError):
        processor._fit_transform(datamodule.df, datamodule)
    with pytest.raises(NotImplementedError):
        processor._transform(datamodule.df, datamodule)


def test_abstract_augmenter():
    pytest_configure_data()
    datamodule = pytest.min_datamodule

    class NotImplementedAugmenter(AbstractAugmenter): ...

    augmenter = NotImplementedAugmenter()
    with pytest.raises(NotImplementedError):
        augmenter._get_augmented(datamodule.df, datamodule)


def test_abstract_selector():
    pytest_configure_data()
    datamodule = pytest.min_datamodule

    class NotImplementedSelector(AbstractFeatureSelector): ...

    selector = NotImplementedSelector()
    with pytest.raises(NotImplementedError):
        selector._get_feature_names_out(datamodule.df, datamodule)


def test_abstract_splitter():
    pytest_configure_data()
    datamodule = pytest.min_datamodule

    class NotImplementedSplitter(AbstractSplitter): ...

    splitter = NotImplementedSplitter()
    with pytest.raises(NotImplementedError):
        splitter._split(
            datamodule.df,
            datamodule.cont_feature_names,
            datamodule.cat_feature_names,
            datamodule.label_name,
        )
    with pytest.raises(NotImplementedError):
        splitter._next_cv(
            datamodule.df,
            datamodule.cont_feature_names,
            datamodule.cat_feature_names,
            datamodule.label_name,
            cv=2,
        )
    with pytest.raises(Exception) as err:
        splitter._check_split([[1, 2, 3]], [[4]], [[5]])
    assert "array" in err.value.args[0]
    with pytest.raises(Exception) as err:
        splitter._check_split(np.array([[1, 2, 3]]), np.array([[4]]), np.array([[5]]))
    assert "flatten" in err.value.args[0]
    with pytest.raises(Exception) as err:
        splitter._check_split(np.array([1, 2, 3]), np.array([3]), np.array([5]))
    assert "intersection" in err.value.args[0]
    with pytest.raises(Exception) as err:
        splitter._check_exist(datamodule.df, "TEST", "TEST")
    assert "is not a valid column" in err.value.args[0]
    splitter._check_exist(datamodule.df, "cont_0", "cont_0")

    from tabensemb.data import dataderiver, dataimputer, datasplitter, dataprocessor

    class IllegalSubclass: ...

    dataderiver.deriver_mapping["TEST_ILLEGAL"] = IllegalSubclass
    dataimputer.imputer_mapping["TEST_ILLEGAL"] = IllegalSubclass
    datasplitter.splitter_mapping["TEST_ILLEGAL"] = IllegalSubclass
    dataprocessor.processor_mapping["TEST_ILLEGAL"] = IllegalSubclass
    for func in [
        get_data_imputer,
        get_data_deriver,
        get_data_processor,
        get_data_splitter,
    ]:
        with pytest.raises(Exception) as not_ext_info:
            func("TEST")
        assert "not implemented" in not_ext_info.value.args[0]
        with pytest.raises(Exception) as not_legal_info:
            func("TEST_ILLEGAL")
        assert "subclass" in not_legal_info.value.args[0]


def test_datamodule_utils():
    pytest_configure_data()
    datamodule = pytest.min_datamodule
    datamodule.set_data_splitter(
        ("RandomSplitter", {"train_val_test": [0.6, 0.2, 0.2]})
    )
    datamodule.set_data_splitter("RandomSplitter")
    datamodule.set_data_splitter("RandomSplitter", ratio=[0.6, 0.2, 0.2])

    with pytest.raises(Exception) as err:
        datamodule.set_data_processors(
            [
                ("StandardScaler", {}),
                ("CategoricalOrdinalEncoder", {}),
                ("StandardScaler", {}),
            ]
        )
    assert "More than one AbstractScaler" in err.value.args[0]
    with pytest.raises(Exception) as err:
        datamodule.set_data_processors(
            [("StandardScaler", {}), ("CategoricalOrdinalEncoder", {})]
        )
    assert "The last dataprocessor" in err.value.args[0]

    tensors = datamodule.get_additional_tensors_slice(datamodule.test_indices)
    arrays = list(
        datamodule.get_derived_data_slice(
            datamodule.derived_data, datamodule.test_indices
        ).values()
    )
    assert all([np.allclose(x, y.cpu().numpy()) for x, y in zip(arrays, tensors)])

    tensor = datamodule.get_first_tensor_slice(datamodule.test_indices)
    array = datamodule.scaled_df.loc[
        datamodule.test_indices, datamodule.cont_feature_names
    ].values
    assert np.allclose(tensor.cpu().numpy(), array)

    assert np.all(datamodule.test_indices == datamodule._get_indices("test"))
    with pytest.raises(Exception) as err:
        datamodule._get_indices("TEST")
    assert "not available" in err.value.args[0]

    cont_data, cat_data, label_data = datamodule.divide_from_tabular_dataset(
        datamodule.scaled_df
    )
    assert datamodule.feature_data.equals(cont_data)
    assert datamodule.label_data.equals(label_data)
    assert datamodule.categorical_data.equals(cat_data)


def test_datamodule_data_path():
    pytest_configure_data()
    datamodule = pytest.min_datamodule
    with pytest.raises(Exception) as err:
        datamodule.load_data(data_path="TEST")
    assert "do not exist" in err.value.args[0]
    datamodule.df.to_excel("sample.xlsx", engine="openpyxl", index=False)
    datamodule.df.to_csv("sample.csv", index=False)
    with pytest.raises(Exception) as err:
        datamodule.load_data(data_path="sample")
    assert "Both" in err.value.args[0]
    original = datamodule.df[datamodule.cont_feature_names].copy()
    datamodule.load_data(data_path="sample.xlsx")
    excel_loaded = datamodule.df
    os.remove("sample.csv")
    os.remove("sample.xlsx")
    assert np.allclose(
        original.values, excel_loaded[datamodule.cont_feature_names].values
    )


def test_infer_task():
    def test_once(manual_config):
        config = UserConfig("sample")
        config.merge(manual_config)
        datamodule = DataModule(config=config)
        datamodule.load_data()
        return datamodule

    datamodule = test_once({"label_name": ["target"]})
    assert datamodule.task == "regression"
    assert datamodule.loss == "mse"

    datamodule = test_once({"label_name": ["target"], "task": "regression"})
    assert datamodule.task == "regression"

    datamodule.scaled_df["target"] = [
        pd.Timestamp(20201010) for x in datamodule.df["target"]
    ]
    with pytest.raises(Exception) as err:
        datamodule._infer_task()
    assert "Unrecognized target type" in err.value.args[0]

    datamodule = test_once({"label_name": ["target_binary"]})
    assert datamodule.task == "binary"
    assert datamodule.loss == "cross_entropy"

    datamodule = test_once({"label_name": ["target_multi_class"]})
    assert datamodule.task == "multiclass"
    assert datamodule.loss == "cross_entropy"

    with pytest.raises(Exception) as err:
        _ = test_once({"label_name": ["target_multi_class"], "loss": "TEST"})
    assert "is not supported" in err.value.args[0]

    with pytest.raises(Exception) as err:
        _ = test_once({"label_name": ["target_multi_class"], "task": "TEST"})
    assert "Unsupported task" in err.value.args[0]

    with pytest.raises(Exception) as err:
        with pytest.warns(UserWarning):
            _ = test_once(
                {
                    "label_name": ["target", "target_multi_class"],
                    "task": ["regression", "multiclass"],
                }
            )
    assert "Multiple tasks is not supported" in err.value.args[0]

    with global_setting({"raise_inconsistent_inferred_task": True}):
        with pytest.raises(Exception) as err:
            _ = test_once(
                {
                    "label_name": ["target"],
                    "task": "binary",
                }
            )
        assert "is not consistent with" in err.value.args[0]

    with pytest.raises(Exception) as err:
        with pytest.warns(UserWarning):
            _ = test_once(
                {
                    "label_name": ["target"],
                    "task": "binary",
                }
            )
    assert "The inferred task is regression" in err.value.args[0]

    with pytest.raises(Exception) as err:
        with pytest.warns(UserWarning):
            _ = test_once({"label_name": ["target", "target_multi_class"]})
    assert "Multi-target classification" in err.value.args[0]


def test_infer_loss():
    config = UserConfig("sample")
    datamodule = DataModule(config=config)
    assert datamodule._infer_loss("binary") == "cross_entropy"
    assert datamodule._infer_loss("multiclass") == "cross_entropy"
    assert datamodule._infer_loss("regression") == "mse"

    config.merge({"loss": "mse"})
    datamodule = DataModule(config=config)
    with pytest.raises(Exception) as err:
        _ = datamodule._infer_loss("binary")
    assert "not supported for binary tasks" in err.value.args[0]
    assert datamodule._infer_loss("regression") == "mse"

    config.merge({"loss": ["mse", "mae"]})
    datamodule = DataModule(config=config)
    with pytest.raises(Exception) as err:
        _ = datamodule._infer_loss("binary")
    assert "Multiple losses is not supported" in err.value.args[0]


def test_select_by_value():
    pytest_configure_data()

    datamodule = pytest.min_datamodule
    cat_1 = datamodule.select_by_value({"cat_1": 1})
    assert np.all(datamodule.df.loc[cat_1, "cat_1"] == 1)

    cat_2 = datamodule.select_by_value({"cat_2": [1, 2]})
    assert np.all(
        (datamodule.df.loc[cat_2, "cat_2"] == 1)
        | (datamodule.df.loc[cat_2, "cat_2"] == 2)
    )

    cat_5 = datamodule.select_by_value({"cat_5": "category_1"})
    assert np.all(datamodule.df.loc[cat_5, "cat_5"] == "category_1")

    cont_1 = datamodule.select_by_value({"cont_1": (-0.1, 0.1)})
    assert np.all(np.abs(datamodule.df.loc[cont_1, "cont_1"]) <= 0.1)

    cont_1 = datamodule.select_by_value({"cont_1": 0.0})
    assert len(cont_1) == 0

    cont_1 = datamodule.select_by_value({"cont_1": 0.0}, eps=0.1)
    assert len(cont_1) > 0 and np.all(
        np.abs(datamodule.df.loc[cont_1, "cont_1"]) <= 0.1
    )

    cont_1_df = datamodule.select_by_value(
        {"cont_1": (-0.1, 0.1)},
        df=datamodule.df.loc[datamodule._get_indices(partition="train"), :],
    )
    cont_1_part = datamodule.select_by_value({"cont_1": (-0.1, 0.1)}, partition="train")
    assert len(np.setdiff1d(cont_1_df, datamodule.train_indices)) == 0
    assert np.all(np.abs(datamodule.df.loc[cont_1_df, "cont_1"]) <= 0.1)
    assert np.allclose(cont_1_df, cont_1_part)

    with pytest.raises(Exception) as err:
        datamodule.select_by_value(
            {"cont_1": (-0.1, 0.1)},
            partition="train",
            df=datamodule.df.loc[datamodule._get_indices(partition="train"), :],
        )
    assert "Provide only one of" in err.value.args[0]

    with pytest.raises(Exception) as err:
        datamodule.select_by_value({"cont_1": (-0.1, 0.1, 0.2)})
    assert "Unrecognized selection of" in err.value.args[0]
