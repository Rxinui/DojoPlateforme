import pytest
from vboxmanage.startvm import VBoxManageStartvm

class TestVBoxManageStartvm:

    def setup_method(self):
        self.command = VBoxManageStartvm()

    def teardown_method(self):
        self.command = None

    def test_startvm_dummy_by_vmname(self):
        assert "VBoxManage startvm dummy".split() == self.command.vmname("dummy")

    def test_startvm_dummy_by_uuid(self):
        assert "VBoxManage startvm 6db383d3-a0bc-472c-89c2-9d36d8f0fa20".split() == self.command.uuid("6db383d3-a0bc-472c-89c2-9d36d8f0fa20")

    def test_startvm_dummy_by_vmname_all_type(self):
        assert "VBoxManage startvm dummy --type headless".split() == self.command.vmname("dummy").type("headless")
        assert "VBoxManage startvm dummy --type gui".split() == self.command.vmname("dummy").type("gui")
        assert "VBoxManage startvm dummy --type separate".split() == self.command.vmname("dummy").type("separate")

    def test_startvm_dummy_by_vmname_illegal_type(self):
        with pytest.raises(ValueError) as exc:
            self.command.vmname("dummy").type("illegal")

