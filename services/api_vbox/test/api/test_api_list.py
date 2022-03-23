import requests
import os
import pytest
from requests.auth import AuthBase
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app

class BearerTokenAuth(AuthBase):

    def __init__(self,token: str):
        self.token = token

    def __call__(self, request: requests.Request):
        request.headers['Authorization'] = f"Bearer {self.token}"
        return request


class TestApiList:

    @classmethod
    def setup_class(cls):
        load_dotenv()
        user = {
            "username": "t.api_vbox.scope_1",
            "email": "t.api_vbox.scope_1@dojo.dev",
            "password": "dojotest"
        }
        cls.client = TestClient(app)
        response = requests.post(f"{os.getenv('API_AUTH_URL')}/user/login",json=user)
        if response.status_code == HTTPStatus.OK:
            cls.auth = BearerTokenAuth(response.json()['token'])
        else:
            pytest.fail("Authentication failed.")
        

    def setup_method(self):
        self.response = None

    def test_list_vms(self):
        self.response = self.client.get("/list", params=dict(q="vms"),auth=self.auth)
        assert self.response.status_code == HTTPStatus.ACCEPTED

    def test_list_vms_sort(self):
        self.response = self.client.get("/list", params=dict(q="vms", sort=True),auth=self.auth)
        self.items = self.response.json()["items"]
        assert self.response.status_code == HTTPStatus.ACCEPTED
        assert self.items["sort"]

    def test_list_vms_long(self):
        self.response = self.client.get("/list", params=dict(q="vms", long=True),auth=self.auth)
        self.items = self.response.json()["items"]
        assert self.response.status_code == HTTPStatus.ACCEPTED
        assert self.items["long"]
        if self.items["vms"]:
            self.one_vm = list(self.items["vms"].values()).pop()
            assert self.one_vm.get("name")

    def test_error_list_no_query(self):
        self.response = self.client.get("/list", params=dict(),auth=self.auth)
        assert self.response.status_code == HTTPStatus.BAD_REQUEST

    def test_error_list_wrong_query(self):
        self.response = self.client.get("/list", params=dict(q="wrong"),auth=self.auth)
        assert self.response.status_code == HTTPStatus.BAD_REQUEST

    def test_illegal_user_scope(self):
        user = {
            "username": "t.api_vbox.scope_2",
            "email": "t.api_vbox.scope_2@dojo.dev",
            "password": "dojotest"
        }
        response = requests.post(f"{os.getenv('API_AUTH_URL')}/user/login",json=user)
        if response.status_code == HTTPStatus.OK:
            auth = BearerTokenAuth(response.json()['token'])
            self.response = self.client.get("/list", params=dict(q="vms,runningvms"),auth=auth)
            assert self.response.status_code == HTTPStatus.UNAUTHORIZED

