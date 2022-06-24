import time
from http import HTTPStatus
from typing import Dict
from . import TestApi
from utils import execute_cmd
from vboxmanage import VBoxManageList


class TestApiImport(TestApi):
    @classmethod
    def setup_class(cls):
        super().authenticate(
            {
                "username": "test.api_vbox.kumite",
                "email": "test.api_vbox.kumite@dojo.dev",
                "password": "dojotest",
            }
        )
        cls.ovf = "tinycore.ova"

    @classmethod
    def teardown_class(cls):
        vms = filter(
            lambda vmname: vmname.startswith(cls._create_vmname("")),
            cls._list_vms().values(),
        )

        try:
            for vmuuid in vms:
                cls._delete_vm(vmuuid)
        except Exception:
            pass

    @classmethod
    def _create_vmname(cls, vmname) -> str:
        return "test_api_import." + vmname

    @classmethod
    def _delete_vm(cls, vmname: str) -> int:
        # exit_code = subprocess.call(["VBoxManage", "unregistervm", vmname, "--delete"])
        _, _, exit_code = execute_cmd("test_api_import",["VBoxManage", "unregistervm", vmname, "--delete"])
        if exit_code != 0:
            raise Exception("Error during _delete_vm. Can't delete vm '%s'" % vmname)
        return exit_code

    @classmethod
    def _list_vms(cls) -> Dict[str, str]:
        # output = subprocess.check_output(["VBoxManage", "list", "vms"]).decode("utf-8")
        output, _, _ = execute_cmd("test_api_import",["VBoxManage", "list", "vms"])
        return VBoxManageList.parser.parse_vms(output)

    @classmethod
    def _is_vm_created(cls, vmname: str) -> bool:
        return vmname in cls._list_vms().values()

    def setup_method(self):
        self.response = None
        self.vmname = None

    def test_import_ovf(self):
        self.vmname = self._create_vmname("test-vm")
        ovf_params = {"vmname": self.vmname, "image": self.ovf}
        self.response = self.client.post("/import", auth=self.auth, json=ovf_params)
        assert self.response.status_code == HTTPStatus.ACCEPTED

    def test_error_import_ovf_vmname_already_taken(self):
        self.vmname = self._create_vmname("test-vm")
        ovf_params = {"vmname": self.vmname, "image": self.ovf}
        self.response = self.client.post("/import", auth=self.auth, json=ovf_params)
        assert self.response.status_code == HTTPStatus.CONFLICT

    # def test_import_ovf_with_expires_time(self):
    #     DELTA_PROCESS_TIME = 3
    #     self.vmname = self._create_vmname("test-vm-expires-time")
    #     ovf_params = {"vmname": self.vmname, "image": self.ovf, "expires_in": 15}
    #     self.response = self.client.post("/import", auth=self.auth, json=ovf_params)
    #     assert self.response.status_code == HTTPStatus.ACCEPTED
    #     assert self._is_vm_created(self.vmname)
    #     time.sleep(ovf_params["expires_in"] + DELTA_PROCESS_TIME)
    #     assert not self._is_vm_created(self.vmname)
