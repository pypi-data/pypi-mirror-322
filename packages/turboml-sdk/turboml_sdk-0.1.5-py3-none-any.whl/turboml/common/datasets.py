from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
import inspect
import logging
import re
import time
from typing import TYPE_CHECKING, Callable, Final, Generic, TypeVar

import ibis
from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator,
)

from turboml.common import dataloader
from turboml.common.api import ApiException, api, NotFoundException
from turboml.common.feature_engineering import (
    FeatureEngineering,
    LocalFeatureEngineering,
    get_features,
)
from turboml.common.internal import TbPandas
from turboml.common.protos import output_pb2

from .models import (
    DataDrift,
    Dataset,
    DatasetRegistrationRequest,
    DatasetRegistrationResponse,
    Datatype,
    DatasetField,
    RegisteredSchema,
    TurboMLResourceIdentifier,
    DatasetSchema,
)  # noqa TCH0001
import pandas as pd

if TYPE_CHECKING:
    from google.protobuf import message

DATATYPE_NUMERICAL = Datatype.FLOAT
DATATYPE_CATEGORICAL = Datatype.INT64
DATATYPE_LABEL = Datatype.FLOAT
DATATYPE_KEY = Datatype.STRING
DATATYPE_IMAGE = Datatype.BYTES
DATATYPE_TEXT = Datatype.STRING
DATATYPE_TIMETICK = Datatype.INT64

logger = logging.getLogger("turboml.datasets")


class LocalInputs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    dataframe: pd.DataFrame
    key_field: DatasetField
    time_field: DatasetField | None
    numerical_fields: list[DatasetField]
    categorical_fields: list[DatasetField]
    textual_fields: list[DatasetField]
    imaginal_fields: list[DatasetField]

    @dataclass
    class _FieldMeta:
        name: str
        _type: str
        wanted_dtype: Datatype

    def all_fields_meta(self):
        return (
            [LocalInputs._FieldMeta(self.key_field, "key", DATATYPE_KEY)]
            + [
                LocalInputs._FieldMeta(field, "numerical", DATATYPE_NUMERICAL)
                for field in self.numerical_fields
            ]
            + [
                LocalInputs._FieldMeta(field, "categorical", DATATYPE_CATEGORICAL)
                for field in self.categorical_fields
            ]
            + [
                LocalInputs._FieldMeta(field, "textual", DATATYPE_TEXT)
                for field in self.textual_fields
            ]
            + [
                LocalInputs._FieldMeta(field, "imaginal", DATATYPE_IMAGE)
                for field in self.imaginal_fields
            ]
            + (
                [LocalInputs._FieldMeta(self.time_field, "time", DATATYPE_TIMETICK)]
                if self.time_field
                else []
            )
        )

    @model_validator(mode="after")
    def select_fields(self):
        all_fields_meta = self.all_fields_meta()

        all_field_names = [field.name for field in all_fields_meta]

        # if a field is used in more than one place, we'll raise an error
        if len(all_field_names) != len(set(all_field_names)):
            # figure out duplicates
            duplicates = [
                field for field, count in Counter(all_field_names).items() if count > 1
            ]
            raise ValueError(f"Fields {duplicates} are specified more than once.")

        absent_fields = set(all_field_names) - set(self.dataframe.columns)
        if absent_fields:
            raise ValueError(
                f"Fields {absent_fields} are not present in the dataframe."
            )

        df = pd.DataFrame()
        for field_meta in all_fields_meta:
            name, type_, wanted_dtype = (
                field_meta.name,
                field_meta._type,
                field_meta.wanted_dtype,
            )
            try:
                column = self.dataframe[name]
                assert isinstance(column, pd.Series)
                column = TbPandas.fill_nans_with_default(column)
                column = column.astype(wanted_dtype.to_pandas_dtype())
                df[name] = column
            except Exception as e:
                raise ValueError(
                    f"Failed to convert {type_} field '{name}' to {wanted_dtype}. "
                    f"Error from pandas.astype(): {e!r}"
                ) from e

        self.dataframe = df
        return self

    @model_validator(mode="after")
    def _validate_time_field(self):
        if not self.time_field:
            return self
        time_field_is_datetime64 = pd.api.types.is_datetime64_any_dtype(
            self.dataframe[self.time_field]
        )
        if not time_field_is_datetime64:
            raise ValueError(f"Field '{self.time_field}' is not of a datetime type.")
        return self

    def validate_fields(self, dataframe: pd.DataFrame):
        # TODO: key field?

        for field in self.numerical_fields:
            if not pd.api.types.is_numeric_dtype(dataframe[field]):
                raise ValueError(f"Field '{field}' is not of a numeric type.")

        # QUESTION: why is this commented out?
        # for field in self.categorical_fields:
        #    if not pd.api.types.is_categorical_dtype(dataframe[field]):
        #        raise ValueError(f"Field '{field}' is not of categorical type.")

        for field in self.textual_fields:
            if not pd.api.types.is_string_dtype(dataframe[field]):
                raise ValueError(f"Field '{field}' is not of a textual type.")

        # QUESTION: why is this commented out?
        # for field in self.imaginal_fields:
        #     if not pd.api.types.is_string_dtype(dataframe[field]):
        #         raise ValueError(f"Field '{field}' is not of a imaginal type.")


# NOTE: At most places where we were accepting `Inputs` previously, we should accept `LocalInputs | OnlineInputs`.
# However for the moment I've kept it as `LocalInputs`, which includes `OnlineInputs` as well since we're
# subclassing (for now) and basically load the entire dataset into memory by default.
# At a later point we should change this so that its possible to pass streaming generators
# from online datasets without loading everything into memory.
class OnlineInputs(LocalInputs):
    dataset_id: TurboMLResourceIdentifier


class LocalLabels(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    dataframe: pd.DataFrame
    key_field: DatasetField
    label_field: DatasetField

    @model_validator(mode="after")
    def validate_and_select_label_field(self):
        if self.label_field not in self.dataframe:
            raise ValueError(
                f"Field '{self.label_field}' is not present in the dataframe."
            )
        label_field_is_numeric = pd.api.types.is_numeric_dtype(
            self.dataframe[self.label_field]
        )
        if not label_field_is_numeric:
            raise ValueError(f"Field '{self.label_field}' is not of a numeric type.")
        df = pd.DataFrame()
        df[self.label_field] = self.dataframe[self.label_field].astype(DATATYPE_LABEL)
        df[self.key_field] = self.dataframe[self.key_field].astype(DATATYPE_KEY)
        self.dataframe = df
        return self


class OnlineLabels(LocalLabels):
    dataset_id: TurboMLResourceIdentifier


FE = TypeVar("FE", LocalFeatureEngineering, FeatureEngineering)


class _BaseInMemoryDataset(Generic[FE]):
    _init_key: Final[object] = object()

    def __init__(
        self,
        init_key: object,
        schema: DatasetSchema,
        df: pd.DataFrame,
        key_field: str,
        feature_engineering: Callable[[pd.DataFrame], FE] = LocalFeatureEngineering,
    ):
        if init_key not in [_BaseInMemoryDataset._init_key, OnlineDataset._init_key]:
            raise AssertionError(
                f"Use from_* methods to instantiate {self.__class__.__name__}"
            )
        self.schema = schema
        self.df = df  # The dataset, as it is
        self.key_field = key_field
        self.feature_engineering = feature_engineering(self.df.copy())

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{key}={value}' for key, value in vars(self).items())})"

    @staticmethod
    def from_schema(
        schema: DatasetSchema,
        key_field: str,
        feature_engineering: Callable[[pd.DataFrame], FE] = LocalFeatureEngineering,
    ) -> _BaseInMemoryDataset[FE]:
        return _BaseInMemoryDataset(
            _BaseInMemoryDataset._init_key,
            schema,
            pd.DataFrame(),
            key_field,
            feature_engineering,
        )

    def __getitem__(self, item):
        """
        Returns a new dataset that is a view of the original dataset.
        """
        if not isinstance(item, slice):
            raise NotImplementedError("Only slicing is supported for now")

        df_view = self.df[item].copy()
        fe = self.feature_engineering
        assert isinstance(df_view, pd.DataFrame)
        assert isinstance(fe, LocalFeatureEngineering)

        return _BaseInMemoryDataset(
            _BaseInMemoryDataset._init_key,
            self.schema,
            df_view,
            self.key_field,
            feature_engineering=lambda df: fe.clone_with_df(df),
        )

    def _is_pd_schema_compatible(self, df: pd.DataFrame) -> bool:
        if len(df) == 0:
            raise ValueError("Empty dataframe not allowed")
        return DatasetSchema.from_pd(df) == self.schema

    def add_pd(self, df: pd.DataFrame):
        if not self._is_pd_schema_compatible(df):
            raise ValueError(
                "Schema mismatch: the dataframe does not match the dataset's input schema."
                f" Expected: {self.schema}, got: {DatasetSchema.from_pd(df)}"
            )
        self.df = pd.concat([self.df, df], ignore_index=True)
        self.feature_engineering._update_input_df(self.df.copy())

    def get_model_inputs(
        self,
        numerical_fields: list | None = None,
        categorical_fields: list | None = None,
        textual_fields: list | None = None,
        imaginal_fields: list | None = None,
        time_field: str | None = None,
    ):
        # Normalize
        if numerical_fields is None:
            numerical_fields = []
        if categorical_fields is None:
            categorical_fields = []
        if textual_fields is None:
            textual_fields = []
        if imaginal_fields is None:
            imaginal_fields = []

        return LocalInputs(
            dataframe=self.feature_engineering.local_features_df,
            key_field=self.key_field,
            numerical_fields=numerical_fields,
            categorical_fields=categorical_fields,
            textual_fields=textual_fields,
            imaginal_fields=imaginal_fields,
            time_field=time_field,
        )

    def get_model_labels(self, label_field: str):
        return LocalLabels(
            dataframe=self.feature_engineering.local_features_df,
            key_field=self.key_field,
            label_field=label_field,
        )


class LocalDataset(_BaseInMemoryDataset[LocalFeatureEngineering]):
    """
    LocalDataset represents an in-memory dataset. In-memory datasets can
    be used for local feature engineering experiments, and training local models.
    A LocalDataset can also be upgraded to an OnlineDataset for online feature
    engineering and serving models based on the same data.
    """

    def __getitem__(self, item):
        s = super().__getitem__(item)
        assert isinstance(s, _BaseInMemoryDataset)
        return LocalDataset(
            LocalDataset._init_key,
            s.schema,
            s.df,
            s.key_field,
            feature_engineering=lambda _: s.feature_engineering,
        )

    def __len__(self):
        return len(self.df)

    @staticmethod
    def from_pd(
        df: pd.DataFrame,
        key_field: str,
    ) -> LocalDataset:
        if len(df) == 0:
            raise ValueError("Empty dataframe")
        schema = DatasetSchema.from_pd(df)
        return LocalDataset(LocalDataset._init_key, schema, df, key_field)

    def to_online(self, id: str, load_if_exists: bool = False) -> OnlineDataset:
        return OnlineDataset.from_local_dataset(self, id, load_if_exists)


class _InMemoryDatasetOnlineFE(_BaseInMemoryDataset[FeatureEngineering]):
    pass


class OnlineDataset:
    """
    OnlineDataset represents a dataset managed and stored by the TurboML platform.
    In addition to operations available on LocalDataset, an online dataset can be
    used to "materialize" engineered features, register and monitor drift, and
    serve models based on the data.
    """

    _init_key = object()

    def __init__(
        self,
        dataset_id: str,
        init_key: object,
        key_field: str,
        protobuf_cls: type[message.Message],
        registered_schema: RegisteredSchema,
        fe: LocalFeatureEngineering | None = None,
    ):
        if init_key is not OnlineDataset._init_key:
            raise AssertionError(
                f"Use load() or from_*() methods to instantiate {self.__class__.__name__}"
            )

        def feature_engineering(df: pd.DataFrame):
            if fe:
                return FeatureEngineering.inherit_from_local(fe, dataset_id)
            return FeatureEngineering(dataset_id, df)

        self.__local_dataset = _InMemoryDatasetOnlineFE.from_schema(
            registered_schema.native_schema,
            key_field=key_field,
            feature_engineering=feature_engineering,
        )

        self.dataset_id = dataset_id
        self.protobuf_cls = protobuf_cls
        self.registered_schema = registered_schema

    @property
    def schema(self):
        return self.__local_dataset.schema

    @property
    def key_field(self):
        return self.__local_dataset.key_field

    @property
    def feature_engineering(self):
        return self.__local_dataset.feature_engineering

    @property
    def preview_df(self):
        return self.__local_dataset.df

    def __repr__(self):
        return f"OnlineDataset(id={self.dataset_id}, key_field={self.key_field}, schema={self.schema})"

    @staticmethod
    def load(dataset_id: str) -> OnlineDataset | None:
        try:
            dataset = api.get(f"dataset?dataset_id={dataset_id}").json()
        except NotFoundException:
            return None
        dataset = Dataset(**dataset)
        schema = api.get(f"dataset/{dataset_id}/schema").json()
        schema = RegisteredSchema(**schema)
        protobuf_cls = dataloader.get_protobuf_class(
            schema=schema.schema_body,
            message_name=dataset.message_name,
        )
        if protobuf_cls is None:
            raise ValueError(
                f"Failed to load protobuf message class for message_name={dataset.message_name}, schema={schema.schema_body}"
            )
        online_dataset = OnlineDataset(
            dataset_id=dataset_id,
            key_field=dataset.key,
            init_key=OnlineDataset._init_key,
            protobuf_cls=protobuf_cls,
            registered_schema=schema,
        )
        online_dataset.sync_features()
        return online_dataset

    @staticmethod
    def _register_dataset(
        dataset_id: str, columns: dict[str, Datatype], key_field: str
    ):
        registration_request = DatasetRegistrationRequest(
            dataset_id=dataset_id,
            data_schema=DatasetRegistrationRequest.ExplicitSchema(fields=columns),
            key_field=key_field,
        )
        try:
            response = api.post("dataset", json=registration_request.model_dump())
        except ApiException as e:
            if "already exists" in str(e):
                raise ValueError(
                    f"Dataset with ID '{dataset_id}' already exists. Use OnlineDataset.load() to load it or specify a different ID."
                ) from e
            raise

        return DatasetRegistrationResponse(**response.json())

    @staticmethod
    def from_local_dataset(
        dataset: LocalDataset, dataset_id: str, load_if_exists: bool = False
    ) -> OnlineDataset:
        if load_if_exists and (online_dataset := OnlineDataset.load(dataset_id)):
            if online_dataset.schema != dataset.schema:
                raise ValueError(
                    f"Dataset already exists with different schema: {online_dataset.schema} != {dataset.schema}"
                )
            return online_dataset
        try:
            response = OnlineDataset._register_dataset(
                dataset_id, dataset.schema.fields, dataset.key_field
            )
        except ApiException as e:
            raise Exception(f"Failed to register dataset: {e!r}") from e

        protobuf_cls = dataloader.get_protobuf_class(
            schema=response.registered_schema.schema_body,
            message_name=response.registered_schema.message_name,
        )
        if protobuf_cls is None:
            raise ValueError(
                f"Failed to load protobuf message class for message_name={response.registered_schema.message_name},"
                f" schema={response.registered_schema.schema_body}"
            )
        online_dataset = OnlineDataset(
            dataset_id=dataset_id,
            key_field=dataset.key_field,
            init_key=OnlineDataset._init_key,
            registered_schema=response.registered_schema,
            protobuf_cls=protobuf_cls,
        )
        try:
            online_dataset.add_pd(dataset.df)
        except Exception as e:
            raise ValueError(f"Failed to push dataset: {e!r}") from e
            # TODO: cleanup ops
        logger.info(
            f"Pushed dataset {online_dataset.dataset_id}. Note that any feature definitions will have to be materialized before they can be used with online models."
        )
        return online_dataset

    def add_pd(self, df: pd.DataFrame):
        if not self.__local_dataset._is_pd_schema_compatible(df):
            raise ValueError(
                "Schema mismatch: the dataframe does not match the dataset's input schema."
                f" Expected: {self.schema}, got: {DatasetSchema.from_pd(df)}"
            )
        try:
            dataloader.upload_df(
                self.dataset_id, df, self.registered_schema, self.protobuf_cls
            )
        except Exception as e:
            raise ValueError(f"Failed to upload data: {e!r}") from e

        # TODO:
        # We really shouldn't maintain a local copy of the dataset
        # or its features. Instead we should support a way to iterate through the dataset
        # or derived featuresets in a streaming fashion, for example by using a generator
        # Still, we should make it so the preview_df is populated by the latest few thousand rows
        old_len = len(self.preview_df)
        while True:
            self.sync_features()
            if len(self.preview_df) > old_len:
                break
            time.sleep(0.5)

    def add_row_dict(self, row: dict):
        raise NotImplementedError  # TODO: complete

    @staticmethod
    def from_pd(
        df: pd.DataFrame, id: str, key_field: str, load_if_exists: bool = False
    ) -> OnlineDataset:
        if load_if_exists and (dataset := OnlineDataset.load(id)):
            return dataset
        df_schema = DatasetSchema.from_pd(df)
        OnlineDataset._register_dataset(id, df_schema.fields, key_field)
        dataset = OnlineDataset.load(id)
        assert dataset is not None
        dataset.add_pd(df)
        return dataset

    # -- fn

    def sync_features(self):
        features_df = get_features(self.dataset_id)
        input_df = features_df[list(self.schema.fields.keys())].copy()
        assert isinstance(input_df, pd.DataFrame)
        self.__local_dataset.df = input_df
        self.__local_dataset.feature_engineering._update_input_df(features_df)

    def to_ibis(self):
        """
        Converts the dataset into an Ibis table.

        Returns:
            ibis.expr.types.Table: An Ibis in-memory table representing the features
            associated with the given dataset_id.

        Raises:
            Exception: If any error occurs during the retrieval of the table name,
            features, or conversion to Ibis table.
        """
        try:
            df = get_features(self.dataset_id)
            return ibis.memtable(df, name=self.dataset_id)
        except Exception as e:
            raise e

    def register_univariate_drift(self, numerical_field: str, label: str | None = None):
        if not numerical_field:
            raise Exception("Numerical field not specified")

        payload = DataDrift(label=label, numerical_fields=[numerical_field])
        api.put(endpoint=f"dataset/{self.dataset_id}/drift", json=payload.model_dump())

    def register_multivariate_drift(self, numerical_fields: list[str], label: str):
        payload = DataDrift(label=label, numerical_fields=numerical_fields)
        api.put(endpoint=f"dataset/{self.dataset_id}/drift", json=payload.model_dump())

    def get_univariate_drift(
        self,
        label: str | None = None,
        numerical_field: str | None = None,
        limit: int = -1,
    ):
        if numerical_field is None and label is None:
            raise Exception("Numerical field and label both cannot be None")

        if numerical_field is not None and label is None:
            label = self._get_default_mv_drift_label([numerical_field])

        return dataloader.get_proto_msgs(
            dataloader.StreamType.UNIVARIATE_DRIFT,
            self.dataset_id,
            output_pb2.Output,
            numeric_feature=label,
        )

    def get_multivariate_drift(
        self,
        label: str | None = None,
        numerical_fields: list[str] | None = None,
        limit: int = -1,
    ):
        if numerical_fields is None and label is None:
            raise Exception("Numerical fields and label both cannot be None")

        if numerical_fields is not None and label is None:
            label = self._get_default_mv_drift_label(numerical_fields)

        return dataloader.get_proto_msgs(
            dataloader.StreamType.MULTIVARIATE_DRIFT,
            self.dataset_id,
            output_pb2.Output,
            label=label,
        )

    def _get_default_mv_drift_label(self, numerical_fields: list[str]):
        payload = DataDrift(numerical_fields=numerical_fields, label=None)

        drift_label = api.get(
            f"dataset/{self.dataset_id}/drift_label", json=payload.model_dump()
        ).json()["label"]

        return drift_label

    def get_model_labels(self, label_field: str):
        local_labels = self.__local_dataset.get_model_labels(label_field)
        return OnlineLabels(
            dataset_id=self.dataset_id,
            **local_labels.model_dump(),
        )

    def get_model_inputs(
        self,
        numerical_fields: list[str] | None = None,
        categorical_fields: list[str] | None = None,
        textual_fields: list[str] | None = None,
        imaginal_fields: list[str] | None = None,
        time_field: str | None = None,
    ):
        local_inputs = self.__local_dataset.get_model_inputs(
            numerical_fields=numerical_fields,
            categorical_fields=categorical_fields,
            textual_fields=textual_fields,
            imaginal_fields=imaginal_fields,
            time_field=time_field,
        )
        return OnlineInputs(
            dataset_id=self.dataset_id,
            **local_inputs.model_dump(),
        )


class PandasHelpers:
    @staticmethod
    def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize a dataframe by removing NaNs and replacing them with type-default values"""
        norm_df = pd.DataFrame()
        for cname in df.columns:
            col = df[cname]
            assert isinstance(col, pd.Series)
            norm_df[cname] = TbPandas.fill_nans_with_default(col)
        return norm_df


DATA_BASE_URL = (
    "https://raw.githubusercontent.com/TurboML-Inc/colab-notebooks/refs/heads/+data/"
)


class StandardDataset(LocalDataset):
    """
    Base class for standard datasets used in our docs.
    """

    @property
    def description(self):
        assert self.__doc__ is not None, "No docstring"
        desc = re.split(pattern=r"\w+\n\s{4}\-{3,}", string=self.__doc__, maxsplit=0)[0]
        return inspect.cleandoc(desc)

    def __repr__(self):
        NEWLINE = "\n"
        schema_k_v = (f"{i[0]}: {i[1]}" for i in self.schema.fields.items())
        return f"""{self.description}


  Samples  {len(self)}
  Schema   {(NEWLINE + 11 * " ").join(schema_k_v)}
"""


# TODO: cache these datasets on disk (/tmp/turboml/datasets) to avoid downloading them
# every time in CI etc


class FraudDetectionDatasetFeatures(StandardDataset):
    """Fraud Detection - Features

    The dataset contains a total of 200,000 fraudulent and non-fraudulent transactions
    described by 22 features. The corresponding labels are available in the FraudDetectionDatasetLabels dataset.
    """

    def __init__(
        self,
    ):
        tx_df = pd.read_csv(f"{DATA_BASE_URL}/transactions.csv")
        schema = DatasetSchema.from_pd(tx_df)
        super().__init__(self._init_key, schema, tx_df, "transactionID")


class FraudDetectionDatasetLabels(StandardDataset):
    """Fraud Detection - Labels

    The dataset contains a total of 200,000 fraudulent and non-fraudulent transactions.
    The corresponding features are available in the FraudDetectionDatasetFeatures dataset.
    """

    def __init__(self):
        labels_df = pd.read_csv(f"{DATA_BASE_URL}/labels.csv")
        schema = DatasetSchema.from_pd(labels_df)
        super().__init__(self._init_key, schema, labels_df, "transactionID")


_credit_cards_df = None


def _load_credit_cards_dataset():
    global _credit_cards_df
    if _credit_cards_df is not None:
        return _credit_cards_df

    try:
        from river import datasets
    except ImportError:
        raise ImportError(
            "The river library is required to load the CreditCards dataset. "
            "Please install it using `pip install river`."
        ) from None
    cc_feats = []
    cc_labels = []
    for sample, score in datasets.CreditCard():
        cc_feats.append(sample)
        cc_labels.append({"score": score})

    feats_df = pd.DataFrame(cc_feats).reset_index()
    labels_df = pd.DataFrame(cc_labels).reset_index()
    _credit_cards_df = pd.merge(feats_df, labels_df, on="index")
    return _credit_cards_df


class CreditCardsDatasetFeatures(StandardDataset):
    """Credit card frauds - Features

    The dataset contains labels for transactions made by credit cards in September 2013 by european
    cardholders. The dataset presents transactions that occurred in two days, where 492
    out of the 284,807 transactions are fraudulent. The dataset is highly unbalanced, the positive class
    (frauds) account for 0.172% of all transactions.

    The corresponding labels are available in CreditCardsDatasetLabels.

    Dataset source: River (https://riverml.xyz)
    """

    def __init__(self):
        try:
            df = _load_credit_cards_dataset()
        except ImportError as e:
            raise e
        df = df.drop(columns=["score"])
        schema = DatasetSchema.from_pd(df)
        super().__init__(self._init_key, schema, df, "index")


class CreditCardsDatasetLabels(StandardDataset):
    """Credit card frauds - Labels

    The dataset contains labels for transactions made by credit cards in September 2013 by european
    cardholders. The dataset presents transactions that occurred in two days, where 492
    out of the 284,807 transactions are fraudulent. The dataset is highly unbalanced, the positive class
    (frauds) account for 0.172% of all transactions.

    The corresponding features are available in CreditCardsDatasetLabels.

    Dataset source: River (https://riverml.xyz)
    """

    def __init__(self):
        try:
            df = _load_credit_cards_dataset()
        except ImportError as e:
            raise e
        df = df[["index", "score"]]
        assert isinstance(df, pd.DataFrame)
        schema = DatasetSchema.from_pd(df)
        super().__init__(self._init_key, schema, df, "index")
