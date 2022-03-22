import requests
import os
from http import HTTPStatus
from dotenv import load_dotenv
class TestApiList:

    @classmethod
    def setup_class(cls):
        load_dotenv()
        cls.host = "https://" if os.environ['API_VBOX_PORT'] == "443" else "http://"
        cls.host += f"{os.environ['API_VBOX_HOST']}:{os.environ['API_VBOX_PORT']}"
        response = requests.post(f"{os.getenv('API_AUTH_URL')}/user/login",json={
            "username": "shihan",
            "email": "shihan@dojo.dev",
            "password": "shihan"
        })
        if response.status_code == HTTPStatus.OK:
            cls.headers = {"Authorization": f"Bearer {response.json()['token']}"}
        

    def setup_method(self):
        self.response = None

    def test_list_vms(self):
        self.response = requests.get(f"{self.host}/list", params=dict(q="vms"),headers=self.headers)
        assert self.response.status_code == HTTPStatus.ACCEPTED

    def test_list_vms_sort(self):
        self.response = requests.get(f"{self.host}/list", params=dict(q="vms", sort=True),headers=self.headers)
        self.items = self.response.json()["items"]
        assert self.response.status_code == HTTPStatus.ACCEPTED
        assert self.items["sort"]

    def test_list_vms_long(self):
        self.response = requests.get(f"{self.host}/list", params=dict(q="vms", long=True),headers=self.headers)
        self.items = self.response.json()["items"]
        assert self.response.status_code == HTTPStatus.ACCEPTED
        assert self.items["long"]
        if self.items["vms"]:
            self.one_vm = list(self.items["vms"].values()).pop()
            assert self.one_vm.get("name")

    def test_error_list_no_query(self):
        self.response = requests.get(f"{self.host}/list", params=dict(),headers=self.headers)
        assert self.response.status_code == HTTPStatus.BAD_REQUEST

    def test_error_list_wrong_query(self):
        self.response = requests.get(f"{self.host}/list", params=dict(q="wrong"),headers=self.headers)
        assert self.response.status_code == HTTPStatus.BAD_REQUEST
