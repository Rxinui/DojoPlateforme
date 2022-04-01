from vboxmanage import VBoxManageBuilder


class TestVBoxManageList:
    def setup_method(self):
        self.builder = VBoxManageBuilder

    def test_vbox_list_vms(self):
        assert "VBoxManage list vms".split() == self.builder.list.vms

    def test_vbox_list_runningvms(self):
        assert (
            "VBoxManage list runningvms -s".split()
            == self.builder.list.runningvms.sort()
        )

    def test_vbox_import_ovf(self):
        assert (
            "VBoxManage import dummy --vsys 0".split()
            == self.builder.import_image.ovf("dummy")
        )

    def test_vbox_import_ovf_vmname_options(self):
        assert "VBoxManage import dummy --vsys 0 --vmname dummyvm --options importtovdi".split() == self.builder.import_image.ovf(
            "dummy"
        ).vmname(
            "dummyvm"
        ).options(
            importtovdi=True
        )
