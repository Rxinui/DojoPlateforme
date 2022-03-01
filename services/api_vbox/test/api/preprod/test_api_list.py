from . import TestApiList

class TestApiListPreprod(TestApiList):

    def test_list_vms(self):
        super().test_list_vms()
        expected = "box-1"
        items = self.response.json()["items"]
        assert expected in items["vms"].values()

    def test_list_vms_sort(self):
        super().test_list_vms_sort()
        
    def test_list_vms_long(self):
        super().test_list_vms_long()
        expected = "box-1"
        assert self.one_vm["name"] == expected