import base64
import logging
from typing import Optional, Callable, Tuple
import itertools

import cloudpickle
from cloudpickle import DEFAULT_PROTOCOL
from pydantic import BaseModel

from turboml.common.datasets import LocalInputs, LocalLabels

from . import namespaces
from . import llm
from .types import PythonModel
from .pytypes import InputData, OutputData
from .datasets import OnlineDataset, LocalDataset
from . import datasets
from .feature_engineering import (
    IbisFeatureEngineering,
    get_timestamp_formats,
    retrieve_features,
    get_features,
)
from .models import (
    AddPythonClassRequest,
    ServiceEndpoints,
    User,
    InputSpec,
    VenvSpec,
    SupervisedAlgorithms,
    UnsupervisedAlgorithms,
    ExternalUdafFunctionSpec,
    UdafFunctionSpec,
    CustomMetric,
)
from .dataloader import (
    upload_df,
    get_proto_msgs,
    get_protobuf_class,
    create_protobuf_from_row_tuple,
    create_protobuf_from_row_dict,
    PROTO_PREFIX_BYTE_LEN,
)
from .api import api
from .concurrent import use_multiprocessing
from .internal import TbPyArrow
from .ml_algs import (
    evaluation_metrics,
    get_default_parameters,
    ml_modelling,
    _resolve_duplicate_columns,
    get_score_for_model,
    RCF,
    HST,
    MStream,
    ONNX,
    HoeffdingTreeClassifier,
    HoeffdingTreeRegressor,
    AMFClassifier,
    AMFRegressor,
    FFMClassifier,
    FFMRegressor,
    SGTClassifier,
    SGTRegressor,
    RandomSampler,
    NNLayer,
    NeuralNetwork,
    Python,
    ONN,
    OVR,
    MultinomialNB,
    GaussianNB,
    AdaptiveXGBoost,
    AdaptiveLGBM,
    MinMaxPreProcessor,
    NormalPreProcessor,
    RobustPreProcessor,
    LlamaCppPreProcessor,
    LlamaTextPreprocess,
    ClipEmbeddingPreprocessor,
    PreProcessor,
    LabelPreProcessor,
    OneHotPreProcessor,
    TargetPreProcessor,
    FrequencyPreProcessor,
    BinaryPreProcessor,
    ImageToNumericPreProcessor,
    SNARIMAX,
    LeveragingBaggingClassifier,
    HeteroLeveragingBaggingClassifier,
    AdaBoostClassifier,
    HeteroAdaBoostClassifier,
    BanditModelSelection,
    ContextualBanditModelSelection,
    RandomProjectionEmbedding,
    LLAMAEmbedding,
    LlamaText,
    ClipEmbedding,
    RestAPIClient,
    EmbeddingModel,
    Model,
    DeployedModel,
    PythonEnsembleModel,
    GRPCClient,
    LocalModel,
)
from .model_comparison import compare_model_metrics
from .sources import DataSource
from .udf import ModelMetricAggregateFunction
from .env import CONFIG

logger = logging.getLogger("turboml.common")


retrieve_model = Model.retrieve_model

__all__ = [
    "init",
    "use_multiprocessing",
    "IbisFeatureEngineering",
    "get_timestamp_formats",
    "upload_df",
    "register_source",
    "register_custom_metric",
    "get_protobuf_class",
    "create_protobuf_from_row_tuple",
    "create_protobuf_from_row_dict",
    "retrieve_features",
    "get_features",
    "set_onnx_model",
    "ml_modelling",
    "setup_venv",
    "get_proto_msgs",
    "ml_algorithms",
    "evaluation_metrics",
    "get_default_parameters",
    "hyperparameter_tuning",
    "algorithm_tuning",
    "compare_model_metrics",
    "login",
    "get_user_info",
    "InputSpec",
    "RCF",
    "HST",
    "MStream",
    "ONNX",
    "HoeffdingTreeClassifier",
    "HoeffdingTreeRegressor",
    "AMFClassifier",
    "AMFRegressor",
    "FFMClassifier",
    "FFMRegressor",
    "SGTClassifier",
    "SGTRegressor",
    "RandomSampler",
    "NNLayer",
    "NeuralNetwork",
    "Python",
    "PythonEnsembleModel",
    "ONN",
    "OVR",
    "MultinomialNB",
    "GaussianNB",
    "AdaptiveXGBoost",
    "AdaptiveLGBM",
    "MinMaxPreProcessor",
    "NormalPreProcessor",
    "RobustPreProcessor",
    "LlamaCppPreProcessor",
    "LlamaTextPreprocess",
    "ClipEmbeddingPreprocessor",
    "PreProcessor",
    "LabelPreProcessor",
    "OneHotPreProcessor",
    "TargetPreProcessor",
    "FrequencyPreProcessor",
    "BinaryPreProcessor",
    "ImageToNumericPreProcessor",
    "SNARIMAX",
    "LeveragingBaggingClassifier",
    "HeteroLeveragingBaggingClassifier",
    "AdaBoostClassifier",
    "HeteroAdaBoostClassifier",
    "BanditModelSelection",
    "ContextualBanditModelSelection",
    "RandomProjectionEmbedding",
    "LLAMAEmbedding",
    "LlamaText",
    "ClipEmbedding",
    "RestAPIClient",
    "EmbeddingModel",
    "retrieve_model",
    "DeployedModel",
    "GRPCClient",
    "namespaces",
    "llm",
    "LocalModel",
    "PROTO_PREFIX_BYTE_LEN",
    "OnlineDataset",
    "LocalDataset",
    "datasets",
]


def ml_algorithms(have_labels: bool) -> list[str]:
    if have_labels:
        algs = [enum.value for enum in SupervisedAlgorithms]
    else:
        algs = [enum.value for enum in UnsupervisedAlgorithms]

    for alg in algs:
        if alg not in globals():
            raise Exception(f"{alg} class doesn't exist")
        elif alg not in __all__:
            raise Exception(f"{alg} class hasn't been exposed")

    return algs


def login(
    api_key: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
):
    """
    Authenticate with the TurboML server.
    The user should provide either the api_key or username, password.
    If a username and password are provided, the api_key will be retrieved from the server.
    Note that instead of login, you can set the TURBOML_API_KEY env variable as well with your api_key.

    Args:
        api_key, username, password (str)
    Raises:
        Exception: Raises an exception if authentication fails.
    """
    api.login(api_key, username, password)


def init(backend_url: str, api_key: str):
    """
    Initialize SDK and Authenticate with TurboML backend server.

    Args:
        backend_url, api_key (str)
    Raises:
        Exception: Raises an exception if authentication fails.
    """
    CONFIG.set_backend_server(backend_url)
    login(api_key=api_key)
    response = api.get("service/endpoints").json()
    service_endpoints = ServiceEndpoints(**response)
    CONFIG.set_feature_server(service_endpoints.feature_server)
    CONFIG.set_arrow_server(service_endpoints.arrow_server)


def get_user_info() -> User:
    resp = api.get("user").json()
    user_info = User(**resp)
    return user_info


def register_source(source: DataSource):
    if not isinstance(source, DataSource):
        raise TypeError("Expected a DataSource, found %s" % type(source))
    api.post(
        endpoint="register_datasource",
        json=source.model_dump(exclude_none=True),
    )


def register_custom_metric(name: str, cls: type[ModelMetricAggregateFunction]):
    """
    Adds a custom model metric to the system.

    This function registers a custom metric class that must extend
    ModelMetricAggregateFunction. The metric class should implement the
    methods 'create_state', 'accumulate', 'merge_states' and 'finish' to calculate the desired metric (e.g., accuracy, AUC, etc.).

    Args:
        name (str): The name used to register and identify the metric.
        cls (Callable[..., ModelMetricAggregateFunction]): The custom metric class
            that should inherit from ModelMetricAggregateFunction.

    Raises:
        TypeError: If `cls` does not inherit from `ModelMetricAggregateFunction`.
    """
    if not issubclass(cls, ModelMetricAggregateFunction):
        raise TypeError(
            f"{cls.__name__} must be a subclass of ModelMetricAggregateFunction."
        )
    spec = ExternalUdafFunctionSpec(obj=base64.b64encode(cloudpickle.dumps(cls)))

    payload = UdafFunctionSpec(name=name, spec=spec, libraries=[])
    headers = {"Content-Type": "application/json"}
    api.post(endpoint="register_udaf", data=payload.model_dump_json(), headers=headers)
    api.post(
        endpoint="register_custom_metric",
        data=CustomMetric(metric_name=name, metric_spec={}).model_dump_json(),
        headers=headers,
    )


def set_onnx_model(input_model: str, onnx_bytes: bytes) -> None:
    """
    input_model: str
        The model name(without the .onnx extension)
    onnx_bytes: bytes
        The model bytes
    """
    api.post(
        endpoint="onnx_model",
        data={"input_model": input_model},
        files={
            "onnx_bytes": (
                f"{input_model}_bytes",
                onnx_bytes,
                "application/octet-stream",
            )
        },
    )


class Venv(BaseModel):
    name: str

    def add_python_file(self, filepath: str):
        """Add a python source file to the system.

        This function registers input source file in the system.

        Args:
            filepath (str): Path of the Python source file.

        Raises:
            Exception: Raises an exception if registering the source with the system fails.
        """
        with open(filepath, "rb") as file:
            files = {"python_file": (filepath, file, "text/x-python")}
            api.post(f"venv/{self.name}/python_source", files=files)

    def add_python_class(
        self, cls: Callable[..., PythonModel], do_validate_as_model: bool = True
    ):
        """
        Add a Python class to the system.
        By default, validates the class as a model by instantiating and calling the init_imports,
        learn_one, and predict_one methods. However this can be disabled with
        do_validate_as_model=False, for instance when the required libraries are not
        available or cannot be installed in the current environment.
        """
        if not isinstance(cls, type):  # Should be a class
            raise ValueError("Input should be a class")
        if do_validate_as_model:
            try:
                Venv._validate_python_model_class(cls)
            except Exception as e:
                raise ValueError(
                    f"{e!r}. HINT: Set do_validate_as_model=False to skip validation if you believe the class is valid."
                ) from e
        serialized_cls = base64.b64encode(
            cloudpickle.dumps(cls, protocol=DEFAULT_PROTOCOL)
        )
        req = AddPythonClassRequest(obj=serialized_cls, name=cls.__name__)
        headers = {"Content-Type": "application/json"}
        api.post(f"venv/{self.name}/class", data=req.model_dump_json(), headers=headers)

    @staticmethod
    def _validate_python_model_class(model_cls: Callable[..., PythonModel]):
        try:
            model = model_cls()
            logger.debug("Model class instantiated successfully")
            init_imports = getattr(model, "init_imports", None)
            if init_imports is None or not callable(init_imports):
                raise ValueError(
                    "Model class must have an init_imports method to import libraries"
                )
            init_imports()
            logger.debug("Model class imports initialized successfully")
            learn_one = getattr(model, "learn_one", None)
            predict_one = getattr(model, "predict_one", None)
            if learn_one is None or not callable(learn_one):
                raise ValueError("Model class must have a learn_one method")
            if predict_one is None or not callable(predict_one):
                raise ValueError("Model class must have a predict_one method")
            # TODO: Once we have the Model.get_dimensions interface in place, use it to determine
            # appropriate input and output shape for the model before passing them to make this check
            # less brittle.
            model.learn_one(InputData.random())
            logger.debug("Model class learn_one method validated successfully")
            model.predict_one(InputData.random(), OutputData.random())
            logger.debug("Model class predict_one method validated successfully")
        except Exception as e:
            # NOTE: We have the
            raise ValueError(f"Model class validation failed: {e!r}") from e


def setup_venv(venv_name: str, lib_list: list[str]) -> Venv:
    """Executes `pip install " ".join(lib_list)` in venv_name virtual environment.
    If venv_name doesn't exist, it'll create one.

    Args:
        venv_name (str): Name of virtual environment
        lib_list (list[str]): List of libraries to install. Will be executed as `pip install " ".join(lib_list)`

    Raises:
        Exception: Raises an exception if setting up the venv fails.
    """
    payload = VenvSpec(venv_name=venv_name, lib_list=lib_list)
    api.post("venv", json=payload.model_dump())
    return Venv(name=venv_name)


def _check_hyperparameter_space(
    hyperparameter_space: list[dict[str, list[str]]], model: Model
):
    model_config = model.get_model_config()

    if len(hyperparameter_space) != len(model_config):
        raise Exception(
            "The number of hyperparameter spaces should be equal to the number of entities in the model."
        )

    for idx in range(len(hyperparameter_space)):
        for key, value in hyperparameter_space[idx].items():
            if key not in model_config[idx]:
                raise Exception(
                    f"Hyperparameter {key} is not a part of the model configuration."
                )
            if not value:
                raise Exception(f"No values provided for hyperparameter {key}.")

        for key, value in model_config[idx].items():
            if key not in hyperparameter_space[idx].keys():
                hyperparameter_space[idx][key] = [value]


SCORE_METRICS = [
    "average_precision",
    "neg_brier_score",
    "neg_log_loss",
    "roc_auc",
    "roc_auc_ovo",
    "roc_auc_ovo_weighted",
    "roc_auc_ovr",
    "roc_auc_ovr_weighted",
]


def hyperparameter_tuning(
    metric_to_optimize: str,
    model: Model,
    hyperparameter_space: list[dict[str, list[str]]],
    input: LocalInputs,
    labels: LocalLabels,
) -> list[Tuple[Model, float]]:
    """
    Perform Hyperparameter Tuning on a model using Grid Search.

    Args:
        metric_to_optimize: str
            The performance metric to be used to find the best model.
        model: turboml.Model
            The model object to be tuned.
        hyperparameter_space: list[dict[str, list[str]]]
            A list of dictionaries specifying the hyperparameters and the corresponding values to be tested for each entity which is a part of `model`.
        input: Inputs
            The input configuration for the models
        labels: Labels
            The label configuration for the models

    Returns:
        list[Tuple[Model, float]]: The list of all models with their corresponding scores sorted in descending order.

    """
    _check_hyperparameter_space(hyperparameter_space, model)

    product_spaces = [
        list(itertools.product(*space.values())) for space in hyperparameter_space
    ]
    combined_product = list(itertools.product(*product_spaces))

    keys = [list(space.keys()) for space in hyperparameter_space]

    hyperparameter_combinations = []
    for product_combination in combined_product:
        combined_dicts = []
        for key_set, value_set in zip(keys, product_combination, strict=False):
            combined_dicts.append(dict(zip(key_set, value_set, strict=False)))
        hyperparameter_combinations.append(combined_dicts)

    return algorithm_tuning(
        [
            Model._construct_model(config, index=0, is_flat=True)[0]
            for config in hyperparameter_combinations
        ],
        metric_to_optimize,
        input,
        labels,
    )


def algorithm_tuning(
    models_to_test: list[Model],
    metric_to_optimize: str,
    input: LocalInputs,
    labels: LocalLabels,
) -> list[Tuple[Model, float]]:
    """
    Test a list of models to find the best model for the given metric.

    Args:
        models_to_test: List[turboml.Model]
            List of models to be tested.
        metric_to_optimize: str
            The performance metric to be used to find the best model.
        input: Inputs
            The input configuration for the models
        labels: Labels
            The label configuration for the models

    Returns:
        list[Tuple[Model, float]]: The list of all models with their corresponding scores sorted in descending order.
    """
    from sklearn import metrics
    import pandas as pd

    if metric_to_optimize not in metrics.get_scorer_names():
        raise Exception(f"{metric_to_optimize} is not yet supported.")
    if not models_to_test:
        raise Exception("No models specified for testing.")

    prediction_column = (
        "score" if metric_to_optimize in SCORE_METRICS else "predicted_class"
    )

    perf_metric = metrics.get_scorer(metric_to_optimize)
    assert isinstance(
        perf_metric, metrics._scorer._Scorer
    ), f"Invalid metric {metric_to_optimize}"

    input_df, label_df = _resolve_duplicate_columns(
        input.dataframe, labels.dataframe, input.key_field
    )
    merged_df = pd.merge(input_df, label_df, on=input.key_field)

    input_spec = InputSpec(
        key_field=input.key_field,
        time_field=input.time_field or "",
        numerical_fields=input.numerical_fields or [],
        categorical_fields=input.categorical_fields or [],
        textual_fields=input.textual_fields or [],
        imaginal_fields=input.imaginal_fields or [],
        label_field=labels.label_field,
    )

    input_table = TbPyArrow.df_to_table(merged_df, input_spec)
    results = []
    for model in models_to_test:
        trained_model, score = get_score_for_model(
            model, input_table, input_spec, labels, perf_metric, prediction_column
        )
        show_model_results(trained_model, score, metric_to_optimize)
        results.append((trained_model, score))

    return sorted(results, key=lambda x: x[1], reverse=True)


def show_model_results(trained_model, score, metric_name):
    """Displays formatted information for a trained model and its performance score."""
    model_name = trained_model.__class__.__name__
    model_params = {
        k: v
        for k, v in trained_model.__dict__.items()
        if not k.startswith("_") and not callable(v)
    }

    params_display = "\n".join(f"  - {k}: {v}" for k, v in model_params.items())

    print(f"\nModel: {model_name}")
    print("Parameters:")
    print(params_display)
    print(f"{metric_name.capitalize()} Score: {score:.5f}\n")
