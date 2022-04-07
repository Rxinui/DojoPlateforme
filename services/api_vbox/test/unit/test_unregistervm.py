from vboxmanage.unregistervm import VBoxManageUnregistervm

class TestVBoxManageUnregistervm:

    def setup_method(self):
        self.command = VBoxManageUnregistervm()

    def teardown_method(self):
        self.command = None

    def test_unregistervm_dummy_by_vmname(self):
        assert "VBoxManage unregistervm dummy".split() == self.command.vmname("dummy")

    def test_unregistervm_dummy_by_vmname_delete(self):
        assert "VBoxManage unregistervm dummy --delete".split() == self.command.vmname("dummy").delete()

    def test_unregistervm_dummy_by_uuid(self):
        assert "VBoxManage unregistervm 6db383d3-a0bc-472c-89c2-9d36d8f0fa20".split() == self.command.uuid("6db383d3-a0bc-472c-89c2-9d36d8f0fa20")

    def test_unregistervm_dummy_by_uuid_delete(self):
        assert "VBoxManage unregistervm 6db383d3-a0bc-472c-89c2-9d36d8f0fa20 --delete".split() == self.command.uuid("6db383d3-a0bc-472c-89c2-9d36d8f0fa20").delete()