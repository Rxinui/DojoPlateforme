from vboxmanage.list import VBoxManageList, VBoxManageListParser


class TestVBoxManageList:
    def setup_method(self):
        self.command = VBoxManageList()

    def teardown_method(self):
        self.command = None

    def test_list_vms(self):
        assert "VBoxManage list vms".split() == self.command.vms

    def test_list_sort_vms(self):
        assert "VBoxManage list vms -s".split() == self.command.vms.sort()

    def test_list_sort_vms_using_apply_options(self):
        assert "VBoxManage list vms -s".split() == self.command.vms.apply_options(
            sort=True, long=False
        )

    def test_list_sort_long_vms(self):
        assert "VBoxManage list vms -s -l".split() == self.command.vms.sort().long()

    def test_list_sort_long_vms_using_apply_options(self):
        assert "VBoxManage list vms -s -l".split() == self.command.vms.apply_options(
            sort=True, long=True
        )

    def test_list_runningvms(self):
        assert "VBoxManage list runningvms".split() == self.command.runningvms

    def test_list_intnets(self):
        assert "VBoxManage list intnets -l".split() == self.command.intnets.long()

    def test_list_hostinfo(self):
        assert "VBoxManage list hostinfo -l".split() == self.command.hostinfo.long()

    def test_list_groups(self):
        assert "VBoxManage list groups".split() == self.command.groups

    def test_list_systemproperties(self):
        assert (
            "VBoxManage list systemproperties".split() == self.command.systemproperties
        )

    def test_list_bridgedifs(self):
        assert "VBoxManage list bridgedifs".split() == self.command.bridgedifs

    def test_list_hostonlyifs(self):
        assert "VBoxManage list hostonlyifs".split() == self.command.hostonlyifs

    def test_list_natnets(self):
        assert "VBoxManage list natnets".split() == self.command.natnets

    def test_list_dhcpservers(self):
        assert "VBoxManage list dhcpservers".split() == self.command.dhcpservers


class TestVBoxManageListParser:
    @classmethod
    def setup_class(cls):
        cls.parser = VBoxManageListParser()

    def test_parse_vms(self):
        assert not self.parser.parse_vms("")
        assert not self.parser.parse_vms("\n")
        assert self.parser.parse_vms(
            '"pmint_box_dev-1" {77bd1e0e-edc6-47fc-807a-987c296c64dd}\n"pmint_box_dev-2"\
            {29bd1e0e-cnt6-02qp-3zx5-662c172c00pl}\n'
        ) == {
            "77bd1e0e-edc6-47fc-807a-987c296c64dd": "pmint_box_dev-1",
            "29bd1e0e-cnt6-02qp-3zx5-662c172c00pl": "pmint_box_dev-2",
        }

    def test_parse_long_vms(self):
        expected = None
        with open("test/data/test_parse_long_vms.txt", encoding="utf-8") as fp:
            expected = self.parser.parse_vms(fp.read(), long=True)
        assert expected
        assert len(expected) == 2  # 2 vms
        assert len(expected["8648ca3d-24b8-4c94-943f-e0a916e966d2"]) == 111
        assert (
            expected["8648ca3d-24b8-4c94-943f-e0a916e966d2"]["nic_1_settings"]
            == "MTU: 0, Socket (send: 64, receive: 64), TCP Window (send:64, receive: 64)"
        )
        assert (
            expected["77bd1e0e-edc6-47fc-807a-987c296c64dd"]["name"]
            == "pmint_box_dev-1"
        )
        assert expected["77bd1e0e-edc6-47fc-807a-987c296c64dd"]["sata_0_0"] == (
            "/home/ubuntu/.config/VirtualBox/system/virtualbox/vms/pmint_box_dev-1/box-1-disk001"
            ".vmdk (UUID: 4d43ade7-ab39-4340-805a-07a0119e17ac)"
        )
        assert (
            expected["77bd1e0e-edc6-47fc-807a-987c296c64dd"]["paravirt_provider"]
            == "Default"
        )

    def test_parse_runningvms(self):
        assert not self.parser.parse_runningvms("")
        assert not self.parser.parse_runningvms("\n")
        assert self.parser.parse_runningvms(
            '"pmint_box_dev-1" {77bd1e0e-edc6-47fc-807a-987c296c64dd}\n"pmint_box_dev-2"  \
            {29bd1e0e-cnt6-02qp-3zx5-662c172c00pl}\n'
        ) == {
            "77bd1e0e-edc6-47fc-807a-987c296c64dd": "pmint_box_dev-1",
            "29bd1e0e-cnt6-02qp-3zx5-662c172c00pl": "pmint_box_dev-2",
        }
        assert self.parser.parse_runningvms(
            '"pmint_box_dev-1" {77bd1e0e-edc6-47fc-807a-987c296c64dd}'
        ) == {"77bd1e0e-edc6-47fc-807a-987c296c64dd": "pmint_box_dev-1"}

    def test_parse_hostinfo(self):
        expected = None
        with open("test/data/test_parse_hostinfo.txt", encoding="utf-8") as fp:
            expected = self.parser.parse_hostinfo(fp.read())
        assert expected
        assert (
            "host_information:\n\n" not in expected
            or "Host Information:\n\n" not in expected
        )
        assert expected["processor#0_speed"] == "3800 MHz"
        assert expected["operating_system_version"] == "5.4.0-92-generic"
