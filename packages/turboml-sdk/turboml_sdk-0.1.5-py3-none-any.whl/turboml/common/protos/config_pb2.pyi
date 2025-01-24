from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MStreamConfig(_message.Message):
    __slots__ = ("num_rows", "num_buckets", "factor")
    NUM_ROWS_FIELD_NUMBER: _ClassVar[int]
    NUM_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    num_rows: int
    num_buckets: int
    factor: float
    def __init__(self, num_rows: _Optional[int] = ..., num_buckets: _Optional[int] = ..., factor: _Optional[float] = ...) -> None: ...

class RCFConfig(_message.Message):
    __slots__ = ("time_decay", "number_of_trees", "output_after", "sample_size")
    TIME_DECAY_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_TREES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_AFTER_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_SIZE_FIELD_NUMBER: _ClassVar[int]
    time_decay: float
    number_of_trees: int
    output_after: int
    sample_size: int
    def __init__(self, time_decay: _Optional[float] = ..., number_of_trees: _Optional[int] = ..., output_after: _Optional[int] = ..., sample_size: _Optional[int] = ...) -> None: ...

class HSTConfig(_message.Message):
    __slots__ = ("n_trees", "height", "window_size")
    N_TREES_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WINDOW_SIZE_FIELD_NUMBER: _ClassVar[int]
    n_trees: int
    height: int
    window_size: int
    def __init__(self, n_trees: _Optional[int] = ..., height: _Optional[int] = ..., window_size: _Optional[int] = ...) -> None: ...

class ONNXConfig(_message.Message):
    __slots__ = ("model_save_name", "model_data")
    MODEL_SAVE_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_DATA_FIELD_NUMBER: _ClassVar[int]
    model_save_name: str
    model_data: bytes
    def __init__(self, model_save_name: _Optional[str] = ..., model_data: _Optional[bytes] = ...) -> None: ...

class HoeffdingClassifierConfig(_message.Message):
    __slots__ = ("delta", "tau", "grace_period", "n_classes", "leaf_pred_method", "split_method")
    DELTA_FIELD_NUMBER: _ClassVar[int]
    TAU_FIELD_NUMBER: _ClassVar[int]
    GRACE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    LEAF_PRED_METHOD_FIELD_NUMBER: _ClassVar[int]
    SPLIT_METHOD_FIELD_NUMBER: _ClassVar[int]
    delta: float
    tau: float
    grace_period: int
    n_classes: int
    leaf_pred_method: str
    split_method: str
    def __init__(self, delta: _Optional[float] = ..., tau: _Optional[float] = ..., grace_period: _Optional[int] = ..., n_classes: _Optional[int] = ..., leaf_pred_method: _Optional[str] = ..., split_method: _Optional[str] = ...) -> None: ...

class HoeffdingRegressorConfig(_message.Message):
    __slots__ = ("delta", "tau", "grace_period", "leaf_pred_method")
    DELTA_FIELD_NUMBER: _ClassVar[int]
    TAU_FIELD_NUMBER: _ClassVar[int]
    GRACE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    LEAF_PRED_METHOD_FIELD_NUMBER: _ClassVar[int]
    delta: float
    tau: float
    grace_period: int
    leaf_pred_method: str
    def __init__(self, delta: _Optional[float] = ..., tau: _Optional[float] = ..., grace_period: _Optional[int] = ..., leaf_pred_method: _Optional[str] = ...) -> None: ...

class AMFClassifierConfig(_message.Message):
    __slots__ = ("n_classes", "n_estimators", "step", "use_aggregation", "dirichlet", "split_pure")
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    N_ESTIMATORS_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    USE_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    DIRICHLET_FIELD_NUMBER: _ClassVar[int]
    SPLIT_PURE_FIELD_NUMBER: _ClassVar[int]
    n_classes: int
    n_estimators: int
    step: float
    use_aggregation: bool
    dirichlet: float
    split_pure: bool
    def __init__(self, n_classes: _Optional[int] = ..., n_estimators: _Optional[int] = ..., step: _Optional[float] = ..., use_aggregation: bool = ..., dirichlet: _Optional[float] = ..., split_pure: bool = ...) -> None: ...

class AMFRegressorConfig(_message.Message):
    __slots__ = ("n_estimators", "step", "use_aggregation", "dirichlet")
    N_ESTIMATORS_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    USE_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    DIRICHLET_FIELD_NUMBER: _ClassVar[int]
    n_estimators: int
    step: float
    use_aggregation: bool
    dirichlet: float
    def __init__(self, n_estimators: _Optional[int] = ..., step: _Optional[float] = ..., use_aggregation: bool = ..., dirichlet: _Optional[float] = ...) -> None: ...

class FFMClassifierConfig(_message.Message):
    __slots__ = ("n_factors", "l1_weight", "l2_weight", "l1_latent", "l2_latent", "intercept", "intercept_lr", "clip_gradient")
    N_FACTORS_FIELD_NUMBER: _ClassVar[int]
    L1_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    L2_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    L1_LATENT_FIELD_NUMBER: _ClassVar[int]
    L2_LATENT_FIELD_NUMBER: _ClassVar[int]
    INTERCEPT_FIELD_NUMBER: _ClassVar[int]
    INTERCEPT_LR_FIELD_NUMBER: _ClassVar[int]
    CLIP_GRADIENT_FIELD_NUMBER: _ClassVar[int]
    n_factors: int
    l1_weight: float
    l2_weight: float
    l1_latent: float
    l2_latent: float
    intercept: float
    intercept_lr: float
    clip_gradient: float
    def __init__(self, n_factors: _Optional[int] = ..., l1_weight: _Optional[float] = ..., l2_weight: _Optional[float] = ..., l1_latent: _Optional[float] = ..., l2_latent: _Optional[float] = ..., intercept: _Optional[float] = ..., intercept_lr: _Optional[float] = ..., clip_gradient: _Optional[float] = ...) -> None: ...

class FFMRegressorConfig(_message.Message):
    __slots__ = ("n_factors", "l1_weight", "l2_weight", "l1_latent", "l2_latent", "intercept", "intercept_lr", "clip_gradient")
    N_FACTORS_FIELD_NUMBER: _ClassVar[int]
    L1_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    L2_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    L1_LATENT_FIELD_NUMBER: _ClassVar[int]
    L2_LATENT_FIELD_NUMBER: _ClassVar[int]
    INTERCEPT_FIELD_NUMBER: _ClassVar[int]
    INTERCEPT_LR_FIELD_NUMBER: _ClassVar[int]
    CLIP_GRADIENT_FIELD_NUMBER: _ClassVar[int]
    n_factors: int
    l1_weight: float
    l2_weight: float
    l1_latent: float
    l2_latent: float
    intercept: float
    intercept_lr: float
    clip_gradient: float
    def __init__(self, n_factors: _Optional[int] = ..., l1_weight: _Optional[float] = ..., l2_weight: _Optional[float] = ..., l1_latent: _Optional[float] = ..., l2_latent: _Optional[float] = ..., intercept: _Optional[float] = ..., intercept_lr: _Optional[float] = ..., clip_gradient: _Optional[float] = ...) -> None: ...

class SNARIMAXConfig(_message.Message):
    __slots__ = ("horizon", "p", "d", "q", "m", "sp", "sd", "sq", "num_children")
    HORIZON_FIELD_NUMBER: _ClassVar[int]
    P_FIELD_NUMBER: _ClassVar[int]
    D_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    M_FIELD_NUMBER: _ClassVar[int]
    SP_FIELD_NUMBER: _ClassVar[int]
    SD_FIELD_NUMBER: _ClassVar[int]
    SQ_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    horizon: int
    p: int
    d: int
    q: int
    m: int
    sp: int
    sd: int
    sq: int
    num_children: int
    def __init__(self, horizon: _Optional[int] = ..., p: _Optional[int] = ..., d: _Optional[int] = ..., q: _Optional[int] = ..., m: _Optional[int] = ..., sp: _Optional[int] = ..., sd: _Optional[int] = ..., sq: _Optional[int] = ..., num_children: _Optional[int] = ...) -> None: ...

class NeuralNetworkConfig(_message.Message):
    __slots__ = ("layers", "dropout", "loss_function", "optimizer", "learning_rate", "batch_size")
    class NeuralNetworkLayer(_message.Message):
        __slots__ = ("input_size", "output_size", "activation", "dropout", "residual_connections", "use_bias")
        INPUT_SIZE_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_SIZE_FIELD_NUMBER: _ClassVar[int]
        ACTIVATION_FIELD_NUMBER: _ClassVar[int]
        DROPOUT_FIELD_NUMBER: _ClassVar[int]
        RESIDUAL_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
        USE_BIAS_FIELD_NUMBER: _ClassVar[int]
        input_size: int
        output_size: int
        activation: str
        dropout: float
        residual_connections: _containers.RepeatedScalarFieldContainer[int]
        use_bias: bool
        def __init__(self, input_size: _Optional[int] = ..., output_size: _Optional[int] = ..., activation: _Optional[str] = ..., dropout: _Optional[float] = ..., residual_connections: _Optional[_Iterable[int]] = ..., use_bias: bool = ...) -> None: ...
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    DROPOUT_FIELD_NUMBER: _ClassVar[int]
    LOSS_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZER_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    layers: _containers.RepeatedCompositeFieldContainer[NeuralNetworkConfig.NeuralNetworkLayer]
    dropout: float
    loss_function: str
    optimizer: str
    learning_rate: float
    batch_size: int
    def __init__(self, layers: _Optional[_Iterable[_Union[NeuralNetworkConfig.NeuralNetworkLayer, _Mapping]]] = ..., dropout: _Optional[float] = ..., loss_function: _Optional[str] = ..., optimizer: _Optional[str] = ..., learning_rate: _Optional[float] = ..., batch_size: _Optional[int] = ...) -> None: ...

class ONNConfig(_message.Message):
    __slots__ = ("max_num_hidden_layers", "qtd_neuron_hidden_layer", "n_classes", "b", "n", "s")
    MAX_NUM_HIDDEN_LAYERS_FIELD_NUMBER: _ClassVar[int]
    QTD_NEURON_HIDDEN_LAYER_FIELD_NUMBER: _ClassVar[int]
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    max_num_hidden_layers: int
    qtd_neuron_hidden_layer: int
    n_classes: int
    b: float
    n: float
    s: float
    def __init__(self, max_num_hidden_layers: _Optional[int] = ..., qtd_neuron_hidden_layer: _Optional[int] = ..., n_classes: _Optional[int] = ..., b: _Optional[float] = ..., n: _Optional[float] = ..., s: _Optional[float] = ...) -> None: ...

class OVRConfig(_message.Message):
    __slots__ = ("n_classes", "num_children")
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    n_classes: int
    num_children: int
    def __init__(self, n_classes: _Optional[int] = ..., num_children: _Optional[int] = ...) -> None: ...

class RandomProjectionEmbeddingConfig(_message.Message):
    __slots__ = ("n_embeddings", "type_embedding")
    N_EMBEDDINGS_FIELD_NUMBER: _ClassVar[int]
    TYPE_EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    n_embeddings: int
    type_embedding: str
    def __init__(self, n_embeddings: _Optional[int] = ..., type_embedding: _Optional[str] = ...) -> None: ...

class EmbeddingModelConfig(_message.Message):
    __slots__ = ("num_children",)
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    num_children: int
    def __init__(self, num_children: _Optional[int] = ...) -> None: ...

class BanditModelSelectionConfig(_message.Message):
    __slots__ = ("bandit", "metric_name")
    BANDIT_FIELD_NUMBER: _ClassVar[int]
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    bandit: str
    metric_name: str
    def __init__(self, bandit: _Optional[str] = ..., metric_name: _Optional[str] = ...) -> None: ...

class ContextualBanditModelSelectionConfig(_message.Message):
    __slots__ = ("contextualbandit", "metric_name")
    CONTEXTUALBANDIT_FIELD_NUMBER: _ClassVar[int]
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    contextualbandit: str
    metric_name: str
    def __init__(self, contextualbandit: _Optional[str] = ..., metric_name: _Optional[str] = ...) -> None: ...

class LeveragingBaggingClassifierConfig(_message.Message):
    __slots__ = ("n_models", "n_classes", "w", "bagging_method", "seed", "num_children")
    N_MODELS_FIELD_NUMBER: _ClassVar[int]
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    BAGGING_METHOD_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    n_models: int
    n_classes: int
    w: float
    bagging_method: str
    seed: int
    num_children: int
    def __init__(self, n_models: _Optional[int] = ..., n_classes: _Optional[int] = ..., w: _Optional[float] = ..., bagging_method: _Optional[str] = ..., seed: _Optional[int] = ..., num_children: _Optional[int] = ...) -> None: ...

class HeteroLeveragingBaggingClassifierConfig(_message.Message):
    __slots__ = ("n_classes", "w", "bagging_method", "seed", "num_children")
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    BAGGING_METHOD_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    n_classes: int
    w: float
    bagging_method: str
    seed: int
    num_children: int
    def __init__(self, n_classes: _Optional[int] = ..., w: _Optional[float] = ..., bagging_method: _Optional[str] = ..., seed: _Optional[int] = ..., num_children: _Optional[int] = ...) -> None: ...

class AdaBoostClassifierConfig(_message.Message):
    __slots__ = ("n_models", "n_classes", "seed", "num_children")
    N_MODELS_FIELD_NUMBER: _ClassVar[int]
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    n_models: int
    n_classes: int
    seed: int
    num_children: int
    def __init__(self, n_models: _Optional[int] = ..., n_classes: _Optional[int] = ..., seed: _Optional[int] = ..., num_children: _Optional[int] = ...) -> None: ...

class HeteroAdaBoostClassifierConfig(_message.Message):
    __slots__ = ("n_classes", "seed", "num_children")
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    n_classes: int
    seed: int
    num_children: int
    def __init__(self, n_classes: _Optional[int] = ..., seed: _Optional[int] = ..., num_children: _Optional[int] = ...) -> None: ...

class SGTClassifierConfig(_message.Message):
    __slots__ = ("delta", "grace_period", "gamma")
    DELTA_FIELD_NUMBER: _ClassVar[int]
    GRACE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    LAMBDA_FIELD_NUMBER: _ClassVar[int]
    GAMMA_FIELD_NUMBER: _ClassVar[int]
    delta: float
    grace_period: int
    gamma: float
    def __init__(self, delta: _Optional[float] = ..., grace_period: _Optional[int] = ..., gamma: _Optional[float] = ..., **kwargs) -> None: ...

class SGTRegressorConfig(_message.Message):
    __slots__ = ("delta", "grace_period", "gamma")
    DELTA_FIELD_NUMBER: _ClassVar[int]
    GRACE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    LAMBDA_FIELD_NUMBER: _ClassVar[int]
    GAMMA_FIELD_NUMBER: _ClassVar[int]
    delta: float
    grace_period: int
    gamma: float
    def __init__(self, delta: _Optional[float] = ..., grace_period: _Optional[int] = ..., gamma: _Optional[float] = ..., **kwargs) -> None: ...

class RandomSamplerConfig(_message.Message):
    __slots__ = ("n_classes", "desired_dist", "sampling_method", "sampling_rate", "seed", "num_children")
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    DESIRED_DIST_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_METHOD_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_RATE_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    n_classes: int
    desired_dist: _containers.RepeatedScalarFieldContainer[float]
    sampling_method: str
    sampling_rate: float
    seed: int
    num_children: int
    def __init__(self, n_classes: _Optional[int] = ..., desired_dist: _Optional[_Iterable[float]] = ..., sampling_method: _Optional[str] = ..., sampling_rate: _Optional[float] = ..., seed: _Optional[int] = ..., num_children: _Optional[int] = ...) -> None: ...

class MultinomialConfig(_message.Message):
    __slots__ = ("n_classes", "alpha")
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    ALPHA_FIELD_NUMBER: _ClassVar[int]
    n_classes: int
    alpha: float
    def __init__(self, n_classes: _Optional[int] = ..., alpha: _Optional[float] = ...) -> None: ...

class GaussianConfig(_message.Message):
    __slots__ = ("n_classes",)
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    n_classes: int
    def __init__(self, n_classes: _Optional[int] = ...) -> None: ...

class PythonConfig(_message.Message):
    __slots__ = ("module_name", "class_name", "venv_name", "code")
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    VENV_NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    module_name: str
    class_name: str
    venv_name: str
    code: str
    def __init__(self, module_name: _Optional[str] = ..., class_name: _Optional[str] = ..., venv_name: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class PythonEnsembleConfig(_message.Message):
    __slots__ = ("module_name", "class_name", "venv_name", "code")
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    VENV_NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    module_name: str
    class_name: str
    venv_name: str
    code: str
    def __init__(self, module_name: _Optional[str] = ..., class_name: _Optional[str] = ..., venv_name: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class PreProcessorConfig(_message.Message):
    __slots__ = ("preprocessor_name", "text_categories", "num_children", "gguf_model_id", "max_tokens_per_input", "image_sizes", "channel_first")
    PREPROCESSOR_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    GGUF_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_PER_INPUT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_SIZES_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIRST_FIELD_NUMBER: _ClassVar[int]
    preprocessor_name: str
    text_categories: _containers.RepeatedScalarFieldContainer[int]
    num_children: int
    gguf_model_id: str
    max_tokens_per_input: int
    image_sizes: _containers.RepeatedScalarFieldContainer[int]
    channel_first: bool
    def __init__(self, preprocessor_name: _Optional[str] = ..., text_categories: _Optional[_Iterable[int]] = ..., num_children: _Optional[int] = ..., gguf_model_id: _Optional[str] = ..., max_tokens_per_input: _Optional[int] = ..., image_sizes: _Optional[_Iterable[int]] = ..., channel_first: bool = ...) -> None: ...

class AdaptiveXGBoostConfig(_message.Message):
    __slots__ = ("n_classes", "learning_rate", "max_depth", "max_window_size", "min_window_size", "max_buffer", "pre_train", "detect_drift", "use_updater", "trees_per_train", "percent_update_trees")
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    MAX_WINDOW_SIZE_FIELD_NUMBER: _ClassVar[int]
    MIN_WINDOW_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_BUFFER_FIELD_NUMBER: _ClassVar[int]
    PRE_TRAIN_FIELD_NUMBER: _ClassVar[int]
    DETECT_DRIFT_FIELD_NUMBER: _ClassVar[int]
    USE_UPDATER_FIELD_NUMBER: _ClassVar[int]
    TREES_PER_TRAIN_FIELD_NUMBER: _ClassVar[int]
    PERCENT_UPDATE_TREES_FIELD_NUMBER: _ClassVar[int]
    n_classes: int
    learning_rate: float
    max_depth: int
    max_window_size: int
    min_window_size: int
    max_buffer: int
    pre_train: int
    detect_drift: bool
    use_updater: bool
    trees_per_train: int
    percent_update_trees: float
    def __init__(self, n_classes: _Optional[int] = ..., learning_rate: _Optional[float] = ..., max_depth: _Optional[int] = ..., max_window_size: _Optional[int] = ..., min_window_size: _Optional[int] = ..., max_buffer: _Optional[int] = ..., pre_train: _Optional[int] = ..., detect_drift: bool = ..., use_updater: bool = ..., trees_per_train: _Optional[int] = ..., percent_update_trees: _Optional[float] = ...) -> None: ...

class AdaptiveLGBMConfig(_message.Message):
    __slots__ = ("n_classes", "learning_rate", "max_depth", "max_window_size", "min_window_size", "max_buffer", "pre_train", "detect_drift", "use_updater", "trees_per_train")
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    MAX_WINDOW_SIZE_FIELD_NUMBER: _ClassVar[int]
    MIN_WINDOW_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_BUFFER_FIELD_NUMBER: _ClassVar[int]
    PRE_TRAIN_FIELD_NUMBER: _ClassVar[int]
    DETECT_DRIFT_FIELD_NUMBER: _ClassVar[int]
    USE_UPDATER_FIELD_NUMBER: _ClassVar[int]
    TREES_PER_TRAIN_FIELD_NUMBER: _ClassVar[int]
    n_classes: int
    learning_rate: float
    max_depth: int
    max_window_size: int
    min_window_size: int
    max_buffer: int
    pre_train: int
    detect_drift: bool
    use_updater: bool
    trees_per_train: int
    def __init__(self, n_classes: _Optional[int] = ..., learning_rate: _Optional[float] = ..., max_depth: _Optional[int] = ..., max_window_size: _Optional[int] = ..., min_window_size: _Optional[int] = ..., max_buffer: _Optional[int] = ..., pre_train: _Optional[int] = ..., detect_drift: bool = ..., use_updater: bool = ..., trees_per_train: _Optional[int] = ...) -> None: ...

class RestAPIClientConfig(_message.Message):
    __slots__ = ("server_url", "max_retries", "connection_timeout", "max_request_time")
    SERVER_URL_FIELD_NUMBER: _ClassVar[int]
    MAX_RETRIES_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    MAX_REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    server_url: str
    max_retries: int
    connection_timeout: int
    max_request_time: int
    def __init__(self, server_url: _Optional[str] = ..., max_retries: _Optional[int] = ..., connection_timeout: _Optional[int] = ..., max_request_time: _Optional[int] = ...) -> None: ...

class GRPCClientConfig(_message.Message):
    __slots__ = ("server_url", "max_retries", "connection_timeout", "max_request_time")
    SERVER_URL_FIELD_NUMBER: _ClassVar[int]
    MAX_RETRIES_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    MAX_REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    server_url: str
    max_retries: int
    connection_timeout: int
    max_request_time: int
    def __init__(self, server_url: _Optional[str] = ..., max_retries: _Optional[int] = ..., connection_timeout: _Optional[int] = ..., max_request_time: _Optional[int] = ...) -> None: ...

class LLAMAEmbeddingModelConfig(_message.Message):
    __slots__ = ("gguf_model_id", "max_tokens_per_input")
    GGUF_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_PER_INPUT_FIELD_NUMBER: _ClassVar[int]
    gguf_model_id: str
    max_tokens_per_input: int
    def __init__(self, gguf_model_id: _Optional[str] = ..., max_tokens_per_input: _Optional[int] = ...) -> None: ...

class LlamaTextConfig(_message.Message):
    __slots__ = ("gguf_model_id", "num_children")
    GGUF_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    gguf_model_id: str
    num_children: int
    def __init__(self, gguf_model_id: _Optional[str] = ..., num_children: _Optional[int] = ...) -> None: ...

class ClipEmbeddingConfig(_message.Message):
    __slots__ = ("gguf_model_id", "num_children")
    GGUF_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    gguf_model_id: str
    num_children: int
    def __init__(self, gguf_model_id: _Optional[str] = ..., num_children: _Optional[int] = ...) -> None: ...

class ModelConfig(_message.Message):
    __slots__ = ("algorithm", "num_children", "mstream_config", "rcf_config", "hst_config", "onnx_config", "hoeffding_classifier_config", "hoeffding_regressor_config", "amf_classifier_config", "amf_regressor_config", "ffm_classifier_config", "ffm_regressor_config", "snarimax_config", "nn_config", "onn_config", "leveraging_bagging_classifier_config", "adaboost_classifier_config", "random_sampler_config", "bandit_model_selection_config", "contextual_bandit_model_selection_config", "python_config", "preprocessor_config", "ovr_model_selection_config", "random_projection_config", "embedding_model_config", "hetero_leveraging_bagging_classifier_config", "hetero_adaboost_classifier_config", "sgt_classifier_config", "sgt_regressor_config", "multinomial_config", "gaussian_config", "adaptive_xgboost_config", "adaptive_lgbm_config", "llama_embedding_config", "rest_api_client_config", "llama_text_config", "clip_embedding_config", "python_ensemble_config", "grpc_client_config")
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    MSTREAM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    RCF_CONFIG_FIELD_NUMBER: _ClassVar[int]
    HST_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ONNX_CONFIG_FIELD_NUMBER: _ClassVar[int]
    HOEFFDING_CLASSIFIER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    HOEFFDING_REGRESSOR_CONFIG_FIELD_NUMBER: _ClassVar[int]
    AMF_CLASSIFIER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    AMF_REGRESSOR_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FFM_CLASSIFIER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FFM_REGRESSOR_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SNARIMAX_CONFIG_FIELD_NUMBER: _ClassVar[int]
    NN_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ONN_CONFIG_FIELD_NUMBER: _ClassVar[int]
    LEVERAGING_BAGGING_CLASSIFIER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ADABOOST_CLASSIFIER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    RANDOM_SAMPLER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    BANDIT_MODEL_SELECTION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CONTEXTUAL_BANDIT_MODEL_SELECTION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PYTHON_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PREPROCESSOR_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OVR_MODEL_SELECTION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    RANDOM_PROJECTION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_MODEL_CONFIG_FIELD_NUMBER: _ClassVar[int]
    HETERO_LEVERAGING_BAGGING_CLASSIFIER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    HETERO_ADABOOST_CLASSIFIER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SGT_CLASSIFIER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SGT_REGRESSOR_CONFIG_FIELD_NUMBER: _ClassVar[int]
    MULTINOMIAL_CONFIG_FIELD_NUMBER: _ClassVar[int]
    GAUSSIAN_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ADAPTIVE_XGBOOST_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ADAPTIVE_LGBM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    LLAMA_EMBEDDING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    REST_API_CLIENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    LLAMA_TEXT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CLIP_EMBEDDING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PYTHON_ENSEMBLE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    GRPC_CLIENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    algorithm: str
    num_children: int
    mstream_config: MStreamConfig
    rcf_config: RCFConfig
    hst_config: HSTConfig
    onnx_config: ONNXConfig
    hoeffding_classifier_config: HoeffdingClassifierConfig
    hoeffding_regressor_config: HoeffdingRegressorConfig
    amf_classifier_config: AMFClassifierConfig
    amf_regressor_config: AMFRegressorConfig
    ffm_classifier_config: FFMClassifierConfig
    ffm_regressor_config: FFMRegressorConfig
    snarimax_config: SNARIMAXConfig
    nn_config: NeuralNetworkConfig
    onn_config: ONNConfig
    leveraging_bagging_classifier_config: LeveragingBaggingClassifierConfig
    adaboost_classifier_config: AdaBoostClassifierConfig
    random_sampler_config: RandomSamplerConfig
    bandit_model_selection_config: BanditModelSelectionConfig
    contextual_bandit_model_selection_config: ContextualBanditModelSelectionConfig
    python_config: PythonConfig
    preprocessor_config: PreProcessorConfig
    ovr_model_selection_config: OVRConfig
    random_projection_config: RandomProjectionEmbeddingConfig
    embedding_model_config: EmbeddingModelConfig
    hetero_leveraging_bagging_classifier_config: HeteroLeveragingBaggingClassifierConfig
    hetero_adaboost_classifier_config: HeteroAdaBoostClassifierConfig
    sgt_classifier_config: SGTClassifierConfig
    sgt_regressor_config: SGTRegressorConfig
    multinomial_config: MultinomialConfig
    gaussian_config: GaussianConfig
    adaptive_xgboost_config: AdaptiveXGBoostConfig
    adaptive_lgbm_config: AdaptiveLGBMConfig
    llama_embedding_config: LLAMAEmbeddingModelConfig
    rest_api_client_config: RestAPIClientConfig
    llama_text_config: LlamaTextConfig
    clip_embedding_config: ClipEmbeddingConfig
    python_ensemble_config: PythonEnsembleConfig
    grpc_client_config: GRPCClientConfig
    def __init__(self, algorithm: _Optional[str] = ..., num_children: _Optional[int] = ..., mstream_config: _Optional[_Union[MStreamConfig, _Mapping]] = ..., rcf_config: _Optional[_Union[RCFConfig, _Mapping]] = ..., hst_config: _Optional[_Union[HSTConfig, _Mapping]] = ..., onnx_config: _Optional[_Union[ONNXConfig, _Mapping]] = ..., hoeffding_classifier_config: _Optional[_Union[HoeffdingClassifierConfig, _Mapping]] = ..., hoeffding_regressor_config: _Optional[_Union[HoeffdingRegressorConfig, _Mapping]] = ..., amf_classifier_config: _Optional[_Union[AMFClassifierConfig, _Mapping]] = ..., amf_regressor_config: _Optional[_Union[AMFRegressorConfig, _Mapping]] = ..., ffm_classifier_config: _Optional[_Union[FFMClassifierConfig, _Mapping]] = ..., ffm_regressor_config: _Optional[_Union[FFMRegressorConfig, _Mapping]] = ..., snarimax_config: _Optional[_Union[SNARIMAXConfig, _Mapping]] = ..., nn_config: _Optional[_Union[NeuralNetworkConfig, _Mapping]] = ..., onn_config: _Optional[_Union[ONNConfig, _Mapping]] = ..., leveraging_bagging_classifier_config: _Optional[_Union[LeveragingBaggingClassifierConfig, _Mapping]] = ..., adaboost_classifier_config: _Optional[_Union[AdaBoostClassifierConfig, _Mapping]] = ..., random_sampler_config: _Optional[_Union[RandomSamplerConfig, _Mapping]] = ..., bandit_model_selection_config: _Optional[_Union[BanditModelSelectionConfig, _Mapping]] = ..., contextual_bandit_model_selection_config: _Optional[_Union[ContextualBanditModelSelectionConfig, _Mapping]] = ..., python_config: _Optional[_Union[PythonConfig, _Mapping]] = ..., preprocessor_config: _Optional[_Union[PreProcessorConfig, _Mapping]] = ..., ovr_model_selection_config: _Optional[_Union[OVRConfig, _Mapping]] = ..., random_projection_config: _Optional[_Union[RandomProjectionEmbeddingConfig, _Mapping]] = ..., embedding_model_config: _Optional[_Union[EmbeddingModelConfig, _Mapping]] = ..., hetero_leveraging_bagging_classifier_config: _Optional[_Union[HeteroLeveragingBaggingClassifierConfig, _Mapping]] = ..., hetero_adaboost_classifier_config: _Optional[_Union[HeteroAdaBoostClassifierConfig, _Mapping]] = ..., sgt_classifier_config: _Optional[_Union[SGTClassifierConfig, _Mapping]] = ..., sgt_regressor_config: _Optional[_Union[SGTRegressorConfig, _Mapping]] = ..., multinomial_config: _Optional[_Union[MultinomialConfig, _Mapping]] = ..., gaussian_config: _Optional[_Union[GaussianConfig, _Mapping]] = ..., adaptive_xgboost_config: _Optional[_Union[AdaptiveXGBoostConfig, _Mapping]] = ..., adaptive_lgbm_config: _Optional[_Union[AdaptiveLGBMConfig, _Mapping]] = ..., llama_embedding_config: _Optional[_Union[LLAMAEmbeddingModelConfig, _Mapping]] = ..., rest_api_client_config: _Optional[_Union[RestAPIClientConfig, _Mapping]] = ..., llama_text_config: _Optional[_Union[LlamaTextConfig, _Mapping]] = ..., clip_embedding_config: _Optional[_Union[ClipEmbeddingConfig, _Mapping]] = ..., python_ensemble_config: _Optional[_Union[PythonEnsembleConfig, _Mapping]] = ..., grpc_client_config: _Optional[_Union[GRPCClientConfig, _Mapping]] = ...) -> None: ...

class FeatureRetrievalConfig(_message.Message):
    __slots__ = ("sql_statement", "placeholder_cols", "result_cols")
    SQL_STATEMENT_FIELD_NUMBER: _ClassVar[int]
    PLACEHOLDER_COLS_FIELD_NUMBER: _ClassVar[int]
    RESULT_COLS_FIELD_NUMBER: _ClassVar[int]
    sql_statement: str
    placeholder_cols: _containers.RepeatedScalarFieldContainer[str]
    result_cols: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, sql_statement: _Optional[str] = ..., placeholder_cols: _Optional[_Iterable[str]] = ..., result_cols: _Optional[_Iterable[str]] = ...) -> None: ...

class KafkaProducerConfig(_message.Message):
    __slots__ = ("write_topic", "proto_file_name", "proto_message_name", "schema_id")
    WRITE_TOPIC_FIELD_NUMBER: _ClassVar[int]
    PROTO_FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROTO_MESSAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_ID_FIELD_NUMBER: _ClassVar[int]
    write_topic: str
    proto_file_name: str
    proto_message_name: str
    schema_id: int
    def __init__(self, write_topic: _Optional[str] = ..., proto_file_name: _Optional[str] = ..., proto_message_name: _Optional[str] = ..., schema_id: _Optional[int] = ...) -> None: ...

class KafkaConsumerConfig(_message.Message):
    __slots__ = ("read_topic", "proto_file_name", "proto_message_name", "consumer_group")
    READ_TOPIC_FIELD_NUMBER: _ClassVar[int]
    PROTO_FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROTO_MESSAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_GROUP_FIELD_NUMBER: _ClassVar[int]
    read_topic: str
    proto_file_name: str
    proto_message_name: str
    consumer_group: str
    def __init__(self, read_topic: _Optional[str] = ..., proto_file_name: _Optional[str] = ..., proto_message_name: _Optional[str] = ..., consumer_group: _Optional[str] = ...) -> None: ...

class InputConfig(_message.Message):
    __slots__ = ("key_field", "label_field", "numerical", "categorical", "time_tick", "textual", "imaginal")
    KEY_FIELD_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_FIELD_NUMBER: _ClassVar[int]
    NUMERICAL_FIELD_NUMBER: _ClassVar[int]
    CATEGORICAL_FIELD_NUMBER: _ClassVar[int]
    TIME_TICK_FIELD_NUMBER: _ClassVar[int]
    TEXTUAL_FIELD_NUMBER: _ClassVar[int]
    IMAGINAL_FIELD_NUMBER: _ClassVar[int]
    key_field: str
    label_field: str
    numerical: _containers.RepeatedScalarFieldContainer[str]
    categorical: _containers.RepeatedScalarFieldContainer[str]
    time_tick: str
    textual: _containers.RepeatedScalarFieldContainer[str]
    imaginal: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, key_field: _Optional[str] = ..., label_field: _Optional[str] = ..., numerical: _Optional[_Iterable[str]] = ..., categorical: _Optional[_Iterable[str]] = ..., time_tick: _Optional[str] = ..., textual: _Optional[_Iterable[str]] = ..., imaginal: _Optional[_Iterable[str]] = ...) -> None: ...

class LearnerConfig(_message.Message):
    __slots__ = ("predict_workers", "update_batch_size", "synchronization_method")
    PREDICT_WORKERS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    SYNCHRONIZATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    predict_workers: int
    update_batch_size: int
    synchronization_method: str
    def __init__(self, predict_workers: _Optional[int] = ..., update_batch_size: _Optional[int] = ..., synchronization_method: _Optional[str] = ...) -> None: ...

class TurboMLConfig(_message.Message):
    __slots__ = ("brokers", "feat_consumer", "output_producer", "label_consumer", "input_config", "model_configs", "initial_model_id", "api_port", "arrow_port", "feature_retrieval", "combined_producer", "combined_consumer", "learner_config", "fully_qualified_model_name")
    BROKERS_FIELD_NUMBER: _ClassVar[int]
    FEAT_CONSUMER_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_PRODUCER_FIELD_NUMBER: _ClassVar[int]
    LABEL_CONSUMER_FIELD_NUMBER: _ClassVar[int]
    INPUT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    MODEL_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    API_PORT_FIELD_NUMBER: _ClassVar[int]
    ARROW_PORT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_RETRIEVAL_FIELD_NUMBER: _ClassVar[int]
    COMBINED_PRODUCER_FIELD_NUMBER: _ClassVar[int]
    COMBINED_CONSUMER_FIELD_NUMBER: _ClassVar[int]
    LEARNER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FULLY_QUALIFIED_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    brokers: str
    feat_consumer: KafkaConsumerConfig
    output_producer: KafkaProducerConfig
    label_consumer: KafkaConsumerConfig
    input_config: InputConfig
    model_configs: _containers.RepeatedCompositeFieldContainer[ModelConfig]
    initial_model_id: str
    api_port: int
    arrow_port: int
    feature_retrieval: FeatureRetrievalConfig
    combined_producer: KafkaProducerConfig
    combined_consumer: KafkaConsumerConfig
    learner_config: LearnerConfig
    fully_qualified_model_name: str
    def __init__(self, brokers: _Optional[str] = ..., feat_consumer: _Optional[_Union[KafkaConsumerConfig, _Mapping]] = ..., output_producer: _Optional[_Union[KafkaProducerConfig, _Mapping]] = ..., label_consumer: _Optional[_Union[KafkaConsumerConfig, _Mapping]] = ..., input_config: _Optional[_Union[InputConfig, _Mapping]] = ..., model_configs: _Optional[_Iterable[_Union[ModelConfig, _Mapping]]] = ..., initial_model_id: _Optional[str] = ..., api_port: _Optional[int] = ..., arrow_port: _Optional[int] = ..., feature_retrieval: _Optional[_Union[FeatureRetrievalConfig, _Mapping]] = ..., combined_producer: _Optional[_Union[KafkaProducerConfig, _Mapping]] = ..., combined_consumer: _Optional[_Union[KafkaConsumerConfig, _Mapping]] = ..., learner_config: _Optional[_Union[LearnerConfig, _Mapping]] = ..., fully_qualified_model_name: _Optional[str] = ...) -> None: ...

class TrainJobConfig(_message.Message):
    __slots__ = ("initial_model_key", "input_config", "model_configs", "model_name", "version_name")
    INITIAL_MODEL_KEY_FIELD_NUMBER: _ClassVar[int]
    INPUT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    MODEL_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_NAME_FIELD_NUMBER: _ClassVar[int]
    initial_model_key: str
    input_config: InputConfig
    model_configs: _containers.RepeatedCompositeFieldContainer[ModelConfig]
    model_name: str
    version_name: str
    def __init__(self, initial_model_key: _Optional[str] = ..., input_config: _Optional[_Union[InputConfig, _Mapping]] = ..., model_configs: _Optional[_Iterable[_Union[ModelConfig, _Mapping]]] = ..., model_name: _Optional[str] = ..., version_name: _Optional[str] = ...) -> None: ...

class ModelConfigList(_message.Message):
    __slots__ = ("model_configs",)
    MODEL_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    model_configs: _containers.RepeatedCompositeFieldContainer[ModelConfig]
    def __init__(self, model_configs: _Optional[_Iterable[_Union[ModelConfig, _Mapping]]] = ...) -> None: ...
