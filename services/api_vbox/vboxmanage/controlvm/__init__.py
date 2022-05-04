"""
Python builder for VBoxManage 'controlvm' subcommand-line tool.

@author Rxinui
@date 2022-04-19
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-controlvm
"""
from .._vboxcommand import VBoxManageCommand
from ._directives import VBoxManageControlvmDirective


class VBoxManageControlvm(VBoxManageCommand):
    """Python wrapper for `VBoxManage controlvm`."""

    parser = None

    ORIGIN: str = "controlvm"

    def uuid(self, uuid: str) -> VBoxManageControlvmDirective:
        """Specify which vm to control by it's uuid.

        Returns:
            VBoxManageControlvmDirective: _description_
        """
        return VBoxManageControlvmDirective(self, uuid)

    def vmname(self, vmname: str) -> VBoxManageControlvmDirective:
        """Specify which vm to control by it's name.

        Returns:
            VBoxManageControlvmDirective: _description_
        """
        return self.uuid(vmname)
