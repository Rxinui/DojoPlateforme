"""
Python builder for VBoxManage 'unregistervm' subcommand-line tool.

@author Rxinui
@date 2022-04-07
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-unregistervm
"""
from .._vboxcommand import VBoxManageCommand
from ._directives import VBoxManageUnregistervmDirective


class VBoxManageUnregistervm(VBoxManageCommand):
    """Python wrapper for `VBoxManage unregistervm`."""

    parser = None

    ORIGIN: str = "unregistervm"

    def __init__(self) -> None:
        super().__init__()
        self._cmd.append(self.ORIGIN)

    def uuid(self, uuid: str) -> VBoxManageUnregistervmDirective:
        """Specify the vm to unregister by vm's uuid.

        Returns:
            VBoxManageUnregistervmDirective: _description_
        """
        return VBoxManageUnregistervmDirective(self, uuid)

    def vmname(self, vmname: str) -> VBoxManageUnregistervmDirective:
        """Specify the vm to unregister by vm's name.

        Returns:
            VBoxManageUnregistervmDirective: _description_
        """
        return self.uuid(vmname)
