"""
Python directive for VBoxManageStartvm builder.

@author Rxinui
@date 2022-04-07
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-startvm
"""
from typing import Optional, Union
from .._vboxcommand import VBoxManageDirective


class VBoxManageStartvmDirective(VBoxManageDirective):
    """General 'startvm' directive in-one class"""

    TYPES = ["headless", "gui", "separate"]

    def type(self, type_value: str) -> "VBoxManageStartvmDirective":
        """Add 'type' flag to commands.

        Allows to set the way of start of a given vm.

        Args:
            type_value (str): set type of start between "headless", "gui", "separate".

        Returns:
            VBoxManageStartvmDirective: updated directive.
        """
        if type_value not in self.TYPES:
            raise ValueError(
                f"'VBoxManage startvm --type <type_value>' must be {','.join(self.TYPES)}"
            )
        self._set_option("--type", type_value)
        return self

    def putenv(
        self, env_name: str, env_value: Optional[Union[str, int]] = None
    ) -> "VBoxManageStartvmDirective":
        """Add 'putenv' flag to commands.

        Allows to define an env var to the vm.

        Args:
            env_name (str): declare an env
            env_value (Optional[Union[str,int]]): set a value to env

        Returns:
            VBoxManageStartvmDirective: updated directive.
        """
        env = env_name
        if env_value:
            env += f"={env_value}"
        self._set_option("--putenv", env)
        return self
