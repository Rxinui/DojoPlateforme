from vboxmanage.import_ import VBoxManageImport


class TestVBoxManageImport:
    def setup_method(self):
        self.command = VBoxManageImport()

    def teardown_method(self):
        self.command = None

    def test_import_ovf_dummy(self):
        assert "VBoxManage import dummy --vsys 0".split() == self.command.ovf("dummy")

    def test_import_ova_dummy(self):
        assert "VBoxManage import dummy --vsys 0".split() == self.command.ova("dummy")

    def test_import_ova_dummy_path(self):
        assert (
            "VBoxManage import system/path/to/dummy --vsys 0".split()
            == self.command.ovf("system/path/to/dummy")
        )

    def test_import_ovf_dry_run(self):
        assert (
            "VBoxManage import dummy --vsys 0 -n".split()
            == self.command.ovf("dummy").dry_run()
        )

    def test_import_ovf_using_apply_options(self):
        assert (
            "VBoxManage import dummy --vsys 0 -n --cloud --vmname dummyvm".split()
            == self.command.ovf("dummy").apply_options(
                dry_run=True, cloud=True, vmname="dummyvm"
            )
        )

    def test_import_ovf_options_1(self):
        assert (
            "VBoxManage import dummy --vsys 0 --options keepnatmacs".split()
            == self.command.ovf("dummy").options(keepnatmacs=True)
        )

    def test_import_ovf_options_2(self):
        assert (
            "VBoxManage import dummy --vsys 0 --options keepallmacs,keepnatmacs".split()
            == self.command.ovf("dummy").options(keepnatmacs=True, keepallmacs=True)
        )

    def test_import_ovf_using_apply_options_multivalues(self):
        assert "VBoxManage import dummy --vsys 0 -n --vmname dummyvm --options keepnatmacs,importtovdi".split() == self.command.ova(
            "dummy"
        ).apply_options(
            dry_run=True,
            vmname="dummyvm",
            options=dict(keepnatmacs=True, importtovdi=True),
        )

    def test_import_ovf_cloud(self):
        assert (
            "VBoxManage import dummy --vsys 0 --cloud".split()
            == self.command.ovf("dummy").cloud()
        )
