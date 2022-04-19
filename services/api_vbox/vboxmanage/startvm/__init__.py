"""
Python builder for VBoxManage 'startvm' subcommand-line tool.

@author Rxinui
@date 2022-04-07
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-startvm
"""
from .._vboxcommand import VBoxManageCommand
from ._directives import VBoxManageStartvmDirective


class VBoxManageStartvm(VBoxManageCommand):
    """Python wrapper for `VBoxManage startvm`."""

    parser = None

    ORIGIN: str = "startvm"

    def __init__(self) -> None:
        super().__init__()
        self._cmd.append(self.ORIGIN)

    def uuid(self, uuid: str) -> VBoxManageStartvmDirective:
        """Specify which vm to start by it's uuid.

        Returns:
            VBoxManageStartvmDirective: _description_
        """
        return VBoxManageStartvmDirective(self, uuid)

    def vmname(self, vmname: str) -> VBoxManageStartvmDirective:
        """Specify which vm to start by it's name.

        Returns:
            VBoxManageStartvmDirective: _description_
        """
        return self.uuid(vmname)
