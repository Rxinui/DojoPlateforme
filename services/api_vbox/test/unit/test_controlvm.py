from vboxmanage.controlvm import VBoxManageControlvm


class TestVBoxManageControlvm:
    def setup_method(self):
        self.command = VBoxManageControlvm()

    def teardown_method(self):
        self.command = None

    def test_controlvm_dummy_by_vmname_pause(self):
        assert (
            "VBoxManage controlvm dummy pause".split()
            == self.command.vmname("dummy").pause()
        )

    def test_controlvm_dummy_by_uuid_resume(self):
        assert (
            "VBoxManage controlvm 6db383d3-a0bc-472c-89c2-9d36d8f0fa20 resume".split()
            == self.command.uuid("6db383d3-a0bc-472c-89c2-9d36d8f0fa20").resume()
        )

    def test_controlvm_dummy_by_vmname_reset(self):
        assert (
            "VBoxManage controlvm dummy reset".split()
            == self.command.vmname("dummy").reset()
        )

    def test_controlvm_dummy_by_vmname_poweroff(self):
        assert (
            "VBoxManage controlvm dummy poweroff".split()
            == self.command.vmname("dummy").poweroff()
        )

    def test_controlvm_dummy_by_vmname_savestate(self):
        assert (
            "VBoxManage controlvm dummy savestate".split()
            == self.command.vmname("dummy").savestate()
        )

    def test_controlvm_dummy_by_vmname_acpipowerbutton(self):
        assert (
            "VBoxManage controlvm dummy acpipowerbutton".split()
            == self.command.vmname("dummy").acpipowerbutton()
        )

    def test_controlvm_dummy_by_vmname_acpisleepbutton(self):
        assert (
            "VBoxManage controlvm dummy acpisleepbutton".split()
            == self.command.vmname("dummy").acpisleepbutton()
        )
