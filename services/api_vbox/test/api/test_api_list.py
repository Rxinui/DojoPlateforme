from http import HTTPStatus
from . import TestApi


class TestApiList(TestApi):
    @classmethod
    def setup_class(cls):
        super().authenticate(
            {
                "username": "t.api_vbox.scope_1",
                "email": "t.api_vbox.scope_1@dojo.dev",
                "password": "dojotest",
            }
        )

    def setup_method(self):
        self.response = None

    def test_list_vms(self):
        self.response = self.client.get("/list", params=dict(q="vms"), auth=self.auth)
        assert self.response.status_code == HTTPStatus.ACCEPTED

    def test_list_vms_sort(self):
        self.response = self.client.get(
            "/list", params=dict(q="vms", sort=True), auth=self.auth
        )
        self.items = self.response.json()["items"]
        assert self.response.status_code == HTTPStatus.ACCEPTED
        assert self.items["sort"]

    def test_list_vms_long(self):
        self.response = self.client.get(
            "/list", params=dict(q="vms", long=True), auth=self.auth
        )
        self.items = self.response.json()["items"]
        assert self.response.status_code == HTTPStatus.ACCEPTED
        assert self.items["long"]
        if self.items["vms"]:
            self.one_vm = list(self.items["vms"].values()).pop()
            assert self.one_vm.get("name")

    def test_error_list_no_query(self):
        self.response = self.client.get("/list", params=dict(), auth=self.auth)
        assert self.response.status_code == HTTPStatus.BAD_REQUEST

    def test_error_list_wrong_query(self):
        self.response = self.client.get("/list", params=dict(q="wrong"), auth=self.auth)
        assert self.response.status_code == HTTPStatus.BAD_REQUEST

    def test_illegal_user_scope(self):
        auth = self.get_auth(
            {
                "username": "t.api_vbox.scope_2",
                "email": "t.api_vbox.scope_2@dojo.dev",
                "password": "dojotest",
            }
        )
        self.response = self.client.get(
            "/list", params=dict(q="vms,runningvms"), auth=auth
        )
        assert self.response.status_code == HTTPStatus.UNAUTHORIZED
