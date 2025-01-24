from .api import api
from .models import NamespaceAcquisitionRequest


def set_active_namespace(namespace: str) -> None:
    api.set_active_namespace(namespace)


def get_default_namespace() -> str:
    return api.get(endpoint="user/namespace/default").json()


def set_default_namespace(namespace: str) -> None:
    resp = api.put(endpoint=f"user/namespace/default?namespace={namespace}")
    if resp.status_code not in range(200, 300):
        raise Exception(f"Failed to set default namespace: {resp.json()['detail']}")


def acquire_namespace(namespace: str) -> None:
    payload = NamespaceAcquisitionRequest(namespace=namespace)
    resp = api.post(
        endpoint="user/namespace/acquire",
        json=payload.model_dump(),
        exclude_namespace=True,
    )
    if resp.status_code not in range(200, 300):
        raise Exception(f"Failed to acquire namespace: {resp.json()['detail']}")


def list_namespaces(include_shared: bool = False) -> list[str]:
    resp = api.get(endpoint=f"user/namespaces?include_shared={include_shared}")
    if resp.status_code not in range(200, 300):
        raise Exception(f"Failed to list namespaces: {resp.json()['detail']}")
    return resp.json()
