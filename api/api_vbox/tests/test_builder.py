import pytest
from vboxmanage import VBoxManageBuilder


class TestVBoxManageList:

    def test_vbox_list_vms(self):
        assert "VBoxManage list vms".split() == VBoxManageBuilder.list().vms()

    def test_vbox_list_runningvms(self):
        assert "VBoxManage list -s runningvms".split() == VBoxManageBuilder.list().runningvms(sort=True)
