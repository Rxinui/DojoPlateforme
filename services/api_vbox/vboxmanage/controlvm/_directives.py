"""
Python directive for VBoxManageControlvm builder.

@author Rxinui
@date 2022-04-07
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-controlvm
"""

from .._vboxcommand import VBoxManageDirective


class VBoxManageControlvmDirective(VBoxManageDirective):
    """General 'controlvm' directive in-one class"""

    def pause(self, flag: bool = True) -> "VBoxManageControlvmDirective":
        """Add 'pause' flag to controlvm command.

        Args:
            flag (bool, optional): Set 'pause' state. Defaults to True.

        Returns:
            VBoxManageControlvmDirective: updated directive.
        """
        self._set_option('pause',flag)
        return self

    def resume(self, flag: bool = True) -> "VBoxManageControlvmDirective":
        """Add 'resume' flag to controlvm command.

        Args:
            flag (bool, optional): Set 'resume' state. Defaults to True.

        Returns:
            VBoxManageControlvmDirective: updated directive.
        """
        self._set_option('resume',flag)
        return self

    def reset(self, flag: bool = True) -> "VBoxManageControlvmDirective":
        """Add 'reset' flag to controlvm command.

        Args:
            flag (bool, optional): Set 'reset' state. Defaults to True.

        Returns:
            VBoxManageControlvmDirective: updated directive.
        """
        self._set_option('reset',flag)
        return self

    def poweroff(self, flag: bool = True) -> "VBoxManageControlvmDirective":
        """Add 'poweroff' flag to controlvm command.

        Args:
            flag (bool, optional): Set 'poweroff' state. Defaults to True.

        Returns:
            VBoxManageControlvmDirective: updated directive.
        """
        self._set_option('poweroff',flag)
        return self

    def savestate(self, flag: bool = True) -> "VBoxManageControlvmDirective":
        """Add 'savestate' flag to controlvm command.

        Args:
            flag (bool, optional): Set 'savestate' state. Defaults to True.

        Returns:
            VBoxManageControlvmDirective: updated directive.
        """
        self._set_option('savestate',flag)
        return self

    def acpipowerbutton(self, flag: bool = True) -> "VBoxManageControlvmDirective":
        """Add 'acpipowerbutton' flag to controlvm command.

        Args:
            flag (bool, optional): Set 'acpipowerbutton' state. Defaults to True.

        Returns:
            VBoxManageControlvmDirective: updated directive.
        """
        self._set_option('acpipowerbutton',flag)
        return self

    def acpisleepbutton(self, flag: bool = True) -> "VBoxManageControlvmDirective":
        """Add 'acpisleepbutton' flag to controlvm command.

        Args:
            flag (bool, optional): Set 'acpisleepbutton' state. Defaults to True.

        Returns:
            VBoxManageControlvmDirective: updated directive.
        """
        self._set_option('acpisleepbutton',flag)
        return self
