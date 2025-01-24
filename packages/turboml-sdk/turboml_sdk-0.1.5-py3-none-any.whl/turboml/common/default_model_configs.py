from google.protobuf import json_format
from frozendict import frozendict
import copy

from turboml.common.protos import config_pb2


class _DefaultModelConfigs:
    def __init__(self):
        self.default_configs = frozendict(
            {
                "MStream": config_pb2.MStreamConfig(
                    num_rows=2, num_buckets=1024, factor=0.8
                ),
                "RCF": config_pb2.RCFConfig(
                    time_decay=0.000390625,
                    number_of_trees=50,
                    output_after=64,
                    sample_size=256,
                ),
                "HST": config_pb2.HSTConfig(n_trees=20, height=12, window_size=50),
                "HoeffdingTreeClassifier": config_pb2.HoeffdingClassifierConfig(
                    delta=1e-7,
                    tau=0.05,
                    grace_period=200,
                    n_classes=2,
                    leaf_pred_method="mc",
                    split_method="gini",
                ),
                "HoeffdingTreeRegressor": config_pb2.HoeffdingRegressorConfig(
                    delta=1e-7, tau=0.05, grace_period=200, leaf_pred_method="mean"
                ),
                "AMFClassifier": config_pb2.AMFClassifierConfig(
                    n_classes=2,
                    n_estimators=10,
                    step=1,
                    use_aggregation=True,
                    dirichlet=0.5,
                    split_pure=False,
                ),
                "AMFRegressor": config_pb2.AMFRegressorConfig(
                    n_estimators=10,
                    step=1,
                    use_aggregation=True,
                    dirichlet=0.5,
                ),
                "FFMClassifier": config_pb2.FFMClassifierConfig(
                    n_factors=10,
                    l1_weight=0,
                    l2_weight=0,
                    l1_latent=0,
                    l2_latent=0,
                    intercept=0,
                    intercept_lr=0.01,
                    clip_gradient=1e12,
                ),
                "FFMRegressor": config_pb2.FFMRegressorConfig(
                    n_factors=10,
                    l1_weight=0,
                    l2_weight=0,
                    l1_latent=0,
                    l2_latent=0,
                    intercept=0,
                    intercept_lr=0.01,
                    clip_gradient=1e12,
                ),
                "SGTClassifier": config_pb2.SGTClassifierConfig(
                    delta=1e-7,
                    gamma=0.1,
                    grace_period=200,
                    **{"lambda": 0.1},  # HACK: lambda is a reserved keyword in Python
                ),
                "SGTRegressor": config_pb2.SGTRegressorConfig(
                    delta=1e-7,
                    gamma=0.1,
                    grace_period=200,
                    **{"lambda": 0.1},
                ),
                "SNARIMAX": config_pb2.SNARIMAXConfig(
                    horizon=1, p=1, d=1, q=1, m=1, sp=0, sd=0, sq=0
                ),
                "ONNX": config_pb2.ONNXConfig(model_save_name=""),
                "LeveragingBaggingClassifier": config_pb2.LeveragingBaggingClassifierConfig(
                    n_models=10,
                    n_classes=2,
                    w=6,
                    bagging_method="bag",
                    seed=0,
                ),
                "HeteroLeveragingBaggingClassifier": config_pb2.HeteroLeveragingBaggingClassifierConfig(
                    n_classes=2,
                    w=6,
                    bagging_method="bag",
                    seed=0,
                ),
                "AdaBoostClassifier": config_pb2.AdaBoostClassifierConfig(
                    n_models=10,
                    n_classes=2,
                    seed=0,
                ),
                "HeteroAdaBoostClassifier": config_pb2.HeteroAdaBoostClassifierConfig(
                    n_classes=2,
                    seed=0,
                ),
                "RandomSampler": config_pb2.RandomSamplerConfig(
                    n_classes=2,
                    desired_dist=[0.5, 0.5],
                    sampling_method="mixed",
                    sampling_rate=1.0,
                    seed=0,
                ),
                "Python": config_pb2.PythonConfig(
                    module_name="", class_name="", venv_name=""
                ),
                "PythonEnsembleModel": config_pb2.PythonEnsembleConfig(
                    module_name="",
                    class_name="",
                    venv_name="",
                ),
                "PreProcessor": config_pb2.PreProcessorConfig(
                    preprocessor_name="MinMax",
                ),
                "NeuralNetwork": config_pb2.NeuralNetworkConfig(
                    dropout=0,
                    layers=[
                        config_pb2.NeuralNetworkConfig.NeuralNetworkLayer(
                            output_size=64,
                            activation="relu",
                            dropout=0.3,
                            residual_connections=[],
                            use_bias=True,
                        ),
                        config_pb2.NeuralNetworkConfig.NeuralNetworkLayer(
                            output_size=64,
                            activation="relu",
                            dropout=0.3,
                            residual_connections=[],
                            use_bias=True,
                        ),
                        config_pb2.NeuralNetworkConfig.NeuralNetworkLayer(
                            output_size=1,
                            activation="sigmoid",
                            dropout=0.3,
                            residual_connections=[],
                            use_bias=True,
                        ),
                    ],
                    loss_function="mse",
                    learning_rate=1e-2,
                    optimizer="sgd",
                    batch_size=64,
                ),
                "ONN": config_pb2.ONNConfig(
                    max_num_hidden_layers=10,
                    qtd_neuron_hidden_layer=32,
                    n_classes=2,
                    b=0.99,
                    n=0.01,
                    s=0.2,
                ),
                "OVR": config_pb2.OVRConfig(
                    n_classes=2,
                ),
                "BanditModelSelection": config_pb2.BanditModelSelectionConfig(
                    bandit="EpsGreedy",
                    metric_name="WindowedMAE",
                ),
                "ContextualBanditModelSelection": config_pb2.ContextualBanditModelSelectionConfig(
                    contextualbandit="LinTS",
                    metric_name="WindowedMAE",
                ),
                "RandomProjectionEmbedding": config_pb2.RandomProjectionEmbeddingConfig(
                    n_embeddings=2,
                    type_embedding="Gaussian",
                ),
                "EmbeddingModel": config_pb2.EmbeddingModelConfig(),
                "MultinomialNB": config_pb2.MultinomialConfig(n_classes=2, alpha=1.0),
                "GaussianNB": config_pb2.GaussianConfig(
                    n_classes=2,
                ),
                "AdaptiveXGBoost": config_pb2.AdaptiveXGBoostConfig(
                    n_classes=2,
                    learning_rate=0.3,
                    max_depth=6,
                    max_window_size=1000,
                    min_window_size=0,
                    max_buffer=5,
                    pre_train=2,
                    detect_drift=True,
                    use_updater=True,
                    trees_per_train=1,
                    percent_update_trees=1.0,
                ),
                "AdaptiveLGBM": config_pb2.AdaptiveLGBMConfig(
                    n_classes=2,
                    learning_rate=0.3,
                    max_depth=6,
                    max_window_size=1000,
                    min_window_size=0,
                    max_buffer=5,
                    pre_train=2,
                    detect_drift=True,
                    use_updater=True,
                    trees_per_train=1,
                ),
                "LLAMAEmbedding": config_pb2.LLAMAEmbeddingModelConfig(),
                "LlamaText": config_pb2.LlamaTextConfig(),
                "ClipEmbedding": config_pb2.ClipEmbeddingConfig(),
                "RestAPIClient": config_pb2.RestAPIClientConfig(
                    max_retries=3,
                    connection_timeout=10,
                    max_request_time=30,
                ),
                "GRPCClient": config_pb2.GRPCClientConfig(
                    max_retries=3,
                    connection_timeout=10000,
                    max_request_time=30000,
                ),
            }
        )
        self.algo_config_mapping = frozendict(
            {
                "MStream": "mstream_config",
                "RCF": "rcf_config",
                "HST": "hst_config",
                "HoeffdingTreeClassifier": "hoeffding_classifier_config",
                "HoeffdingTreeRegressor": "hoeffding_regressor_config",
                "AMFClassifier": "amf_classifier_config",
                "AMFRegressor": "amf_regressor_config",
                "FFMClassifier": "ffm_classifier_config",
                "SGTClassifier": "sgt_classifier_config",
                "SGTRegressor": "sgt_regressor_config",
                "FFMRegressor": "ffm_regressor_config",
                "SNARIMAX": "snarimax_config",
                "ONNX": "onnx_config",
                "LeveragingBaggingClassifier": "leveraging_bagging_classifier_config",
                "HeteroLeveragingBaggingClassifier": "hetero_leveraging_bagging_classifier_config",
                "AdaBoostClassifier": "adaboost_classifier_config",
                "HeteroAdaBoostClassifier": "hetero_adaboost_classifier_config",
                "RandomSampler": "random_sampler_config",
                "Python": "python_config",
                "PythonEnsembleModel": "python_ensemble_config",
                "PreProcessor": "preprocessor_config",
                "NeuralNetwork": "nn_config",
                "ONN": "onn_config",
                "OVR": "ovr_model_selection_config",
                "BanditModelSelection": "bandit_model_selection_config",
                "ContextualBanditModelSelection": "contextual_bandit_model_selection_config",
                "RandomProjectionEmbedding": "random_projection_config",
                "EmbeddingModel": "embedding_model_config",
                "MultinomialNB": "multinomial_config",
                "GaussianNB": "gaussian_config",
                "AdaptiveXGBoost": "adaptive_xgboost_config",
                "AdaptiveLGBM": "adaptive_lgbm_config",
                "LLAMAEmbedding": "llama_embedding_config",
                "LlamaText": "llama_text_config",
                "ClipEmbedding": "clip_embedding_config",
                "RestAPIClient": "rest_api_client_config",
                "GRPCClient": "grpc_client_config",
            }
        )

    def get_default_parameters(self):
        parameters = {}
        for alg, config in self.default_configs.items():
            parameters[alg] = json_format.MessageToDict(config)
        return parameters

    def fill_config(self, conf: config_pb2.ModelConfig, parameters):
        new_config = json_format.ParseDict(
            parameters, copy.deepcopy(self.default_configs[conf.algorithm])
        )
        try:
            getattr(conf, self.algo_config_mapping[conf.algorithm]).CopyFrom(new_config)
        except Exception as e:
            raise Exception(f"Failed to match config: {conf.algorithm}") from e
        return conf


DefaultModelConfigs = _DefaultModelConfigs()
