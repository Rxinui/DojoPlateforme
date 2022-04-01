import subprocess
from http import HTTPStatus
from . import TestApi


class TestApiImport(TestApi):
    @classmethod
    def setup_class(cls):
        super().authenticate(
            {
                "username": "t.api_vbox.scope_2",
                "email": "t.api_vbox.scope_2@dojo.dev",
                "password": "dojotest",
            }
        )
        cls.ovf = "pmint_box_dev.ova"

    def _delete_vm(self, vmname: str):
        exit_code = subprocess.call(["VBoxManage", "unregistervm", vmname, "--delete"])
        if exit_code != 0:
            raise Exception("Error during _delete_vm. Can't delete vm '%s'" % vmname)
        return exit_code

    def setup_method(self):
        self.response = None
        self.vmname = None

    # def teardown_method(self):
    #     if self.response and self.response.status_code == HTTPStatus.ACCEPTED:
    #         if self._delete_vm(self.vmname) != 0:
    #             raise Exception(
    #                 "Error during teardown. Can't delete vm '%s'" % self.vmname
    #             )

    def test_import_ovf(self):
        self.vmname = "test_api_import.test-vm"
        ovf_params = {"vmname": self.vmname, "image": self.ovf}
        self.response = self.client.post("/import", auth=self.auth, json=ovf_params)
        assert self.response.status_code == HTTPStatus.ACCEPTED

    def test_error_import_ovf_vmname_already_taken(self):
        self.vmname = "test_api_import.test-vm"
        ovf_params = {"vmname": self.vmname, "image": self.ovf}
        self.response = self.client.post("/import", auth=self.auth, json=ovf_params)
        assert self.response.status_code == HTTPStatus.CONFLICT
        self._delete_vm(self.vmname)
