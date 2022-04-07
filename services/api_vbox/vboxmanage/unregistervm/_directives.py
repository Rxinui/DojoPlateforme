"""
Python directive for VBoxManageUnregistervm builder.

@author Rxinui
@date 2022-04-07
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-unregistervm
"""
from .._vboxcommand import VBoxManageDirective


class VBoxManageUnregistervmDirective(VBoxManageDirective):
    """General 'unregistervm' directive in-one class"""

    def delete(self, flag: bool = True) -> "VBoxManageUnregistervmDirective":
        """Add 'delete' flag to commands.

        Allows to delete all files related to the given vm.

        Args:
            flag (bool, optional): enable 'delete'. Defaults to True.

        Returns:
            VBoxManageUnregistervmDirective: updated directive.
        """
        self._set_option("--delete", flag)
        return self
