import requests
import os
from typing import Dict, Union
from http import HTTPStatus
from fastapi.testclient import TestClient
from requests.auth import AuthBase
from dotenv import load_dotenv
from main import app


class BearerTokenAuth(AuthBase):
    def __init__(self, token: str):
        self.token = token

    def __call__(self, request: requests.Request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request

    def __repr__(self) -> str:
        return self.token


class TestApi:
    """Test API utility parent class.

    Contains useful methods for any subclasses `TestApi*`.

    Raises:
        Exception: authentication to `api_auth` failed
    """

    auth_type = BearerTokenAuth

    @classmethod
    def authenticate(cls, user: Dict[str, str]):
        """Initialize authentication client for test.

        Args:
            user (Dict[str, str]): user credentials
        """
        load_dotenv()
        cls.client = TestClient(app)
        cls.auth = cls.get_auth(user)

    @classmethod
    def get_auth_response(cls, user: Dict[str, str]) -> requests.Response:
        """Return authentication response from `api_auth`.

        Args:
            user (Dict[str, str]): user credentials

        Returns:
            requests.Response: auth response
        """
        return requests.post(f"{os.getenv('API_AUTH_URL')}/user/login", json=user)

    @classmethod
    def get_auth(cls, obj: Union[Dict[str, str], requests.Response]) -> AuthBase:
        """Return authentication from `api_auth`.

        Args:
            obj (Union[Dict[str, str], requests.Response]): user

        Raises:
            Exception: authentication failed

        Returns:
            AuthBase: Token auth
        """
        if isinstance(obj, requests.Response):
            return cls.auth_type(obj.json()["token"])
        elif isinstance(obj, dict):
            response = cls.get_auth_response(obj)
            if response.status_code == HTTPStatus.OK:
                return cls.get_auth(response)
            raise Exception("Authentication failed.")
