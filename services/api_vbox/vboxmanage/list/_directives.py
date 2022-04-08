"""
Python directive for VBoxManageList builder.

@author Rxinui
@date 2022-01-21
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-list
"""
from .._vboxcommand import VBoxManageDirective


class VBoxManageListDirective(VBoxManageDirective):

    """General 'list' directive in-one class"""

    def sort(self, flag: bool = True):
        """Add the 'sorted' flag to commands.

        Returns:
            VBoxManageListDirective: updated directive
        """
        self._set_option("-s",flag)
        return self

    def long(self, flag: bool = True):
        """Add the 'long' flag to commands.

        Returns:
            VBoxManageListDirective: updated directive
        """
        self._set_option("-l",flag)
        return self
