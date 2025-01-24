import sources_pb2 as _sources_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FlinkDeploymentResource(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeploymentRequest(_message.Message):
    __slots__ = ("deployment_name", "sql_deployment", "artifact_deployment", "flink_properties", "job_manager_config", "task_manager_config", "env_vars", "from_savepoint", "recreate_on_update", "savepoint", "allow_non_restored_state", "take_savepoint_on_update", "parallelism", "restart_policy", "cleanup_policy", "savepoint_generation", "cancel_requested", "local_time_zone")
    class SqlDeployment(_message.Message):
        __slots__ = ("query", "data_sources", "udfs", "sink_topic", "sink_topic_message_name")
        class Udf(_message.Message):
            __slots__ = ("name", "code")
            NAME_FIELD_NUMBER: _ClassVar[int]
            CODE_FIELD_NUMBER: _ClassVar[int]
            name: str
            code: str
            def __init__(self, name: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...
        QUERY_FIELD_NUMBER: _ClassVar[int]
        DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
        UDFS_FIELD_NUMBER: _ClassVar[int]
        SINK_TOPIC_FIELD_NUMBER: _ClassVar[int]
        SINK_TOPIC_MESSAGE_NAME_FIELD_NUMBER: _ClassVar[int]
        query: str
        data_sources: _containers.RepeatedCompositeFieldContainer[_sources_pb2.DataSource]
        udfs: _containers.RepeatedCompositeFieldContainer[DeploymentRequest.SqlDeployment.Udf]
        sink_topic: str
        sink_topic_message_name: str
        def __init__(self, query: _Optional[str] = ..., data_sources: _Optional[_Iterable[_Union[_sources_pb2.DataSource, _Mapping]]] = ..., udfs: _Optional[_Iterable[_Union[DeploymentRequest.SqlDeployment.Udf, _Mapping]]] = ..., sink_topic: _Optional[str] = ..., sink_topic_message_name: _Optional[str] = ...) -> None: ...
    class ArtifactDeployment(_message.Message):
        __slots__ = ("java_job", "python_job", "files_base_path", "flink_properties")
        class JavaJob(_message.Message):
            __slots__ = ("jar_name", "class_name")
            JAR_NAME_FIELD_NUMBER: _ClassVar[int]
            CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
            jar_name: str
            class_name: str
            def __init__(self, jar_name: _Optional[str] = ..., class_name: _Optional[str] = ...) -> None: ...
        class PythonJob(_message.Message):
            __slots__ = ("file_name",)
            FILE_NAME_FIELD_NUMBER: _ClassVar[int]
            file_name: str
            def __init__(self, file_name: _Optional[str] = ...) -> None: ...
        class FlinkPropertiesEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        JAVA_JOB_FIELD_NUMBER: _ClassVar[int]
        PYTHON_JOB_FIELD_NUMBER: _ClassVar[int]
        FILES_BASE_PATH_FIELD_NUMBER: _ClassVar[int]
        FLINK_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        java_job: DeploymentRequest.ArtifactDeployment.JavaJob
        python_job: DeploymentRequest.ArtifactDeployment.PythonJob
        files_base_path: str
        flink_properties: _containers.ScalarMap[str, str]
        def __init__(self, java_job: _Optional[_Union[DeploymentRequest.ArtifactDeployment.JavaJob, _Mapping]] = ..., python_job: _Optional[_Union[DeploymentRequest.ArtifactDeployment.PythonJob, _Mapping]] = ..., files_base_path: _Optional[str] = ..., flink_properties: _Optional[_Mapping[str, str]] = ...) -> None: ...
    class ContainerResourceLimits(_message.Message):
        __slots__ = ("cpu_limit", "memory_limit")
        CPU_LIMIT_FIELD_NUMBER: _ClassVar[int]
        MEMORY_LIMIT_FIELD_NUMBER: _ClassVar[int]
        cpu_limit: str
        memory_limit: str
        def __init__(self, cpu_limit: _Optional[str] = ..., memory_limit: _Optional[str] = ...) -> None: ...
    class JobManagerConfig(_message.Message):
        __slots__ = ("job_manager_resources_limits", "num_of_replicas")
        JOB_MANAGER_RESOURCES_LIMITS_FIELD_NUMBER: _ClassVar[int]
        NUM_OF_REPLICAS_FIELD_NUMBER: _ClassVar[int]
        job_manager_resources_limits: DeploymentRequest.ContainerResourceLimits
        num_of_replicas: int
        def __init__(self, job_manager_resources_limits: _Optional[_Union[DeploymentRequest.ContainerResourceLimits, _Mapping]] = ..., num_of_replicas: _Optional[int] = ...) -> None: ...
    class TaskManagerConfig(_message.Message):
        __slots__ = ("task_manager_resources_limits", "num_of_replicas")
        TASK_MANAGER_RESOURCES_LIMITS_FIELD_NUMBER: _ClassVar[int]
        NUM_OF_REPLICAS_FIELD_NUMBER: _ClassVar[int]
        task_manager_resources_limits: DeploymentRequest.ContainerResourceLimits
        num_of_replicas: int
        def __init__(self, task_manager_resources_limits: _Optional[_Union[DeploymentRequest.ContainerResourceLimits, _Mapping]] = ..., num_of_replicas: _Optional[int] = ...) -> None: ...
    class Savepoint(_message.Message):
        __slots__ = ("auto_savepoint_seconds", "savepoints_dir")
        AUTO_SAVEPOINT_SECONDS_FIELD_NUMBER: _ClassVar[int]
        SAVEPOINTS_DIR_FIELD_NUMBER: _ClassVar[int]
        auto_savepoint_seconds: int
        savepoints_dir: str
        def __init__(self, auto_savepoint_seconds: _Optional[int] = ..., savepoints_dir: _Optional[str] = ...) -> None: ...
    class FlinkPropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class EnvVarsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DEPLOYMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    SQL_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    FLINK_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    JOB_MANAGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TASK_MANAGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ENV_VARS_FIELD_NUMBER: _ClassVar[int]
    FROM_SAVEPOINT_FIELD_NUMBER: _ClassVar[int]
    RECREATE_ON_UPDATE_FIELD_NUMBER: _ClassVar[int]
    SAVEPOINT_FIELD_NUMBER: _ClassVar[int]
    ALLOW_NON_RESTORED_STATE_FIELD_NUMBER: _ClassVar[int]
    TAKE_SAVEPOINT_ON_UPDATE_FIELD_NUMBER: _ClassVar[int]
    PARALLELISM_FIELD_NUMBER: _ClassVar[int]
    RESTART_POLICY_FIELD_NUMBER: _ClassVar[int]
    CLEANUP_POLICY_FIELD_NUMBER: _ClassVar[int]
    SAVEPOINT_GENERATION_FIELD_NUMBER: _ClassVar[int]
    CANCEL_REQUESTED_FIELD_NUMBER: _ClassVar[int]
    LOCAL_TIME_ZONE_FIELD_NUMBER: _ClassVar[int]
    deployment_name: str
    sql_deployment: DeploymentRequest.SqlDeployment
    artifact_deployment: DeploymentRequest.ArtifactDeployment
    flink_properties: _containers.ScalarMap[str, str]
    job_manager_config: DeploymentRequest.JobManagerConfig
    task_manager_config: DeploymentRequest.TaskManagerConfig
    env_vars: _containers.ScalarMap[str, str]
    from_savepoint: str
    recreate_on_update: bool
    savepoint: DeploymentRequest.Savepoint
    allow_non_restored_state: bool
    take_savepoint_on_update: bool
    parallelism: int
    restart_policy: str
    cleanup_policy: str
    savepoint_generation: int
    cancel_requested: bool
    local_time_zone: str
    def __init__(self, deployment_name: _Optional[str] = ..., sql_deployment: _Optional[_Union[DeploymentRequest.SqlDeployment, _Mapping]] = ..., artifact_deployment: _Optional[_Union[DeploymentRequest.ArtifactDeployment, _Mapping]] = ..., flink_properties: _Optional[_Mapping[str, str]] = ..., job_manager_config: _Optional[_Union[DeploymentRequest.JobManagerConfig, _Mapping]] = ..., task_manager_config: _Optional[_Union[DeploymentRequest.TaskManagerConfig, _Mapping]] = ..., env_vars: _Optional[_Mapping[str, str]] = ..., from_savepoint: _Optional[str] = ..., recreate_on_update: bool = ..., savepoint: _Optional[_Union[DeploymentRequest.Savepoint, _Mapping]] = ..., allow_non_restored_state: bool = ..., take_savepoint_on_update: bool = ..., parallelism: _Optional[int] = ..., restart_policy: _Optional[str] = ..., cleanup_policy: _Optional[str] = ..., savepoint_generation: _Optional[int] = ..., cancel_requested: bool = ..., local_time_zone: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
