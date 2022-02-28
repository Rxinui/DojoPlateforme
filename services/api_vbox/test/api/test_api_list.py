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

    def setup_method(self):
        self.response = None

    def test_list_vms(self):
        self.response = requests.get(f"{self.host}/list", params=dict(q="vms"))
        assert self.response.status_code == HTTPStatus.ACCEPTED

    def test_list_vms_sort(self):
        self.response = requests.get(f"{self.host}/list", params=dict(q="vms", sort=True))
        self.items = self.response.json()["items"]
        assert self.response.status_code == HTTPStatus.ACCEPTED
        assert self.items["sort"]

    def test_list_vms_long(self):
        self.response = requests.get(f"{self.host}/list", params=dict(q="vms", long=True))
        self.items = self.response.json()["items"]
        assert self.response.status_code == HTTPStatus.ACCEPTED
        assert self.items["long"]
        if self.items["vms"]:
            self.one_vm = list(self.items["vms"].values()).pop()
            assert self.one_vm.get("name")

    def test_error_list_no_query(self):
        self.response = requests.get(f"{self.host}/list", params=dict())
        assert self.response.status_code == HTTPStatus.BAD_REQUEST

    def test_error_list_wrong_query(self):
        self.response = requests.get(f"{self.host}/list", params=dict(q="wrong"))
        assert self.response.status_code == HTTPStatus.BAD_REQUEST
