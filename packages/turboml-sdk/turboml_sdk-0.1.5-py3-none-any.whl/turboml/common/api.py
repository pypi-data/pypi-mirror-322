from .env import CONFIG

import os
import logging
from typing import Optional
import time
import requests

import jwt
import tenacity
import uuid


# Refresh access token if it is about to expire in 1 hour
TOKEN_EXPIRY_THRESHOLD = 3600

logger = logging.getLogger(__name__)


class ApiException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

    def __repr__(self):
        return f"{self.__class__.__name__}(message={self.message}, status_code={self.status_code})"

    def __str__(self):
        return self.__repr__()


class NotFoundException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, 404)


class Api:
    def __init__(self):
        self.session = requests.Session()
        self._api_key: Optional[str] = None
        self._access_token: Optional[str] = None
        self._namespace: Optional[str] = None
        if api_key := os.getenv("TURBOML_API_KEY"):
            self._api_key = api_key
        if namespace := os.getenv("TURBOML_ACTIVE_NAMESPACE"):
            self._namespace = namespace
            logger.debug(
                f"Namespace set to '{namespace}' from environment variable 'TURBOML_ACTIVE_NAMESPACE'"
            )
        else:
            logger.debug(
                "No namespace set; 'TURBOML_ACTIVE_NAMESPACE' environment variable not found."
            )

    def clear_session(self):
        self._api_key = None
        self._access_token = None

    def login(
        self,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        if api_key:
            self._api_key = api_key
            resp = self.session.get(
                url=f"{self.API_BASE_ADDRESS}/user",
                headers=self.headers,
            )
            if resp.status_code != 200:
                self._api_key = None
                raise ApiException("Invalid API key", status_code=resp.status_code)
            return
        if username:
            assert password, "Provide a password along with username"
            resp = self.session.post(
                url=f"{self.API_BASE_ADDRESS}/login",
                data={"username": username, "password": password},
            )
            if resp.status_code != 200:
                raise ApiException(
                    "Invalid username/password", status_code=resp.status_code
                )
            self._access_token = resp.json()["access_token"]
            return
        raise ValueError("Provide either an API key or username/password")

    def _refresh_access_token_if_about_to_expire(self) -> None:
        assert self._access_token, "No access token found"
        decoded_jwt = jwt.decode(
            self._access_token,
            algorithms=["HS256"],
            options={"verify_signature": False},
        )
        token_expiry = decoded_jwt.get("exp")
        if token_expiry - time.time() < TOKEN_EXPIRY_THRESHOLD:
            resp = self.session.post(
                url=f"{self.API_BASE_ADDRESS}/renew_token",
                headers={"Authorization": f"Bearer {self._access_token}"},
            )
            if resp.status_code != 200:
                raise ApiException(
                    "Failed to refresh access token try to login in again using login()",
                    status_code=resp.status_code,
                )
            self._access_token = resp.json()["access_token"]

    @property
    def API_BASE_ADDRESS(self) -> str:
        return CONFIG.TURBOML_BACKEND_SERVER_ADDRESS + "/api"

    @property
    def headers(self) -> dict[str, str]:
        headers = {}
        if self._namespace:
            headers["X-Turboml-Namespace"] = self._namespace
        if self._api_key:
            headers["Authorization"] = f"apiKey {self._api_key}"
            return headers
        if self._access_token:
            self._refresh_access_token_if_about_to_expire()
            headers["Authorization"] = f"Bearer {self._access_token}"
            return headers
        raise ValueError("No API key or access token found. Please login first")

    def set_active_namespace(self, namespace: str):
        original_namespace = self._namespace
        self._namespace = namespace
        resp = self.get("user/namespace")
        if resp.status_code not in range(200, 300):
            self._namespace = original_namespace
            raise Exception(f"Failed to set namespace: {resp.json()['detail']}")

    @property
    def arrow_headers(self) -> list[tuple[bytes, bytes]]:
        return [(k.lower().encode(), v.encode()) for k, v in self.headers.items()]

    @property
    def namespace(self) -> str:
        return self.get("user/namespace").json()

    @tenacity.retry(
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=5),
        stop=tenacity.stop_after_attempt(3),
        reraise=True,
    )
    def _request(self, method, url, headers, params, data, json, files):
        resp = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            files=files,
        )
        if resp.status_code == 502:  # Catch and retry on Bad Gateway
            raise Exception("Bad Gateway")
        return resp

    def request(
        self,
        method,
        endpoint,
        host=None,
        data=None,
        params=None,
        json=None,
        files=None,
        headers=None,
        exclude_namespace=False,
    ):
        if not host:
            host = self.API_BASE_ADDRESS
        combined_headers = self.headers.copy()
        if headers:
            combined_headers.update(headers)
        # Exclude the namespace header if requested
        if exclude_namespace:
            combined_headers.pop("X-Turboml-Namespace", None)

        idempotency_key = uuid.uuid4().hex
        combined_headers["Idempotency-Key"] = idempotency_key

        resp = self._request(
            method=method.upper(),
            url=f"{host}/{endpoint}",
            headers=combined_headers,
            params=params,
            data=data,
            json=json,
            files=files,
        )
        if not (200 <= resp.status_code < 300):
            try:
                json_resp = resp.json()
                error_details = json_resp.get("detail", json_resp)
            except ValueError:
                error_details = resp.text
            if resp.status_code == 404:
                raise NotFoundException(error_details)
            raise ApiException(
                error_details,
                status_code=resp.status_code,
            ) from None
        return resp

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def options(self, endpoint, **kwargs):
        return self.request("OPTIONS", endpoint, **kwargs)

    def head(self, endpoint, **kwargs):
        return self.request("HEAD", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)


api = Api()
