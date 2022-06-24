import os
from pathlib import Path
from http import HTTPStatus
from typing import Dict
from . import TestApi
from utils import execute_cmd


class TestApiStartvm(TestApi):
    @classmethod
    def setup_class(cls):
        super().authenticate(
            {
                "username": "t.api_vbox.scope_3",
                "email": "t.api_vbox.scope_3@dojo.dev",
                "password": "dojotest",
            }
        )
        cls.ovf = "ubuntu-server.ova"
        cls.STORAGE_OVF_BASEFOLDER = Path(os.getenv("STORAGE_OVF_BASEFOLDER"))
        cls.STORAGE_VMS_BASEFOLDER = Path(os.getenv("STORAGE_VMS_BASEFOLDER"))
        cls.vmname = "test_api_startvm.tinycore"
        # output, error, exit_code = execute_cmd(
        #     "test_api_starvm",
        #     [
        #         "VBoxManage",
        #         "import",
        #         str(cls.STORAGE_OVF_BASEFOLDER / cls.ovf),
        #         "--vsys",
        #         "0",
        #         "--vmname",
        #         cls.vmname,
        #         "--options",
        #         "keepnatmacs",
        #         "--basefolder",
        #         str(cls.STORAGE_VMS_BASEFOLDER),
        #     ],
        # )
        # if exit_code != 0:
        #     raise SystemError(f"TestApiStartvm.setup_class failed: {error}")

    # @classmethod
    # def teardown_class(cls):
    #     _, _, exit_code = execute_cmd("test_api_startvm",["VBoxManage", "unregistervm", cls.vmname, "--delete"])
    #     if exit_code != 0:
    #         raise Exception("Error during _delete_vm. Can't delete vm '%s'" % cls.vmname)

    def setup_method(self):
        self.response = None

    def test_startvm_simple(self):
        vm_params = {"vmname": self.vmname, "type": "headless"}
        self.response = self.client.post("/startvm", auth=self.auth, json=vm_params)
        print(self.response.content)
        assert self.response.status_code == HTTPStatus.ACCEPTED
