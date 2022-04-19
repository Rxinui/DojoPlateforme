from .unregistervm import VBoxManageUnregistervm
from .list import VBoxManageList
from .import_ import VBoxManageImport
from .startvm import VBoxManageStartvm


class VBoxManageBuilder:
    """
    Python class to build shell VBoxManage commands programatically.
    """

    @classmethod
    @property
    def list(cls) -> VBoxManageList:
        return VBoxManageList()

    @classmethod
    @property
    def import_image(cls) -> VBoxManageImport:
        return VBoxManageImport()

    @classmethod
    @property
    def unregistervm(cls) -> VBoxManageUnregistervm:
        return VBoxManageUnregistervm()

    @classmethod
    @property
    def startvm(cls) -> VBoxManageUnregistervm:
        return VBoxManageUnregistervm()
