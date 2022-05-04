"""Abstract classes for VBoxManage wrapper."""
from abc import ABC
from typing import Dict, List, Optional, Union


class VBoxManageCommand(ABC):

    """
    Command-line CLI used to control VBoxManage
    """

    CLI: str = "VBoxManage"

    ORIGIN: str = None

    def __init__(self) -> None:
        """Initialise VBoxManage command"""
        super().__init__()
        self._cmd = [self.CLI]
        if self.ORIGIN:
            self._cmd.append(self.ORIGIN)

    @property
    def cmd(self) -> List[str]:
        """Commands in constructions.

        Returns:
            List[str]: command terms
        """
        return self._cmd.copy()

    def __repr__(self) -> List[str]:
        """Represent a VBoxManageCommand as a list of terms.

        Returns:
            List[str]: command terms
        """
        return list.__repr__(self._cmd)

    def __eq__(self, __o: object) -> bool:
        """Equality of VBoxManageCommand is the same equality of a list.

        Args:
            __o (object): list to compare

        Returns:
            bool: True if the VBoxManagaCommand has the same
                  ordered terms than {__o} else False.
        """
        return list.__eq__(self._cmd, __o)


class VBoxManageDirective(VBoxManageCommand, ABC):

    """
    Directive of VBoxManageCommand
    """

    def __init__(self, vbox_command: VBoxManageCommand, directive: str) -> None:
        """Initialise VBoxManage command"""
        super().__init__()
        self._cmd = vbox_command.cmd + [directive]
        self._options = {}
        self._options_order = []

    def _set_option(self, flag: str, value: Union[str, bool, int]):
        """Set option in self._options dict and keep the order of set.

        Args:
            flag (str): option flag
            value (Union[str,bool,int]): option value
        """
        self._options[flag] = value
        if flag not in self._options_order and value is not False:
            self._options_order.append(flag)

    def apply_options(
        self, **kwargs: Optional[Dict[str, Union[str, List[str], Dict]]]
    ) -> "VBoxManageDirective":
        """General method to apply defined options declared within the class.

        Returns:
            VBoxManageDirective: updated directive with options passed
        """
        for flag, value in kwargs.items():
            if isinstance(value, dict):
                self.__getattribute__(flag)(**value)
            else:
                self.__getattribute__(flag)(value)
        return self

    def build(self) -> List[str]:
        """Build command terms as a list of string.

        The built command will be used as Shell-command

        Returns:
            List[str]: command as a list of string
        """
        _options = []
        for flag, value in self._options.items():
            _options.append(flag)
            if value is False:
                _options.pop()
            if not isinstance(value, bool):
                _options.append(value)
        return self._cmd + _options

    def __repr__(self) -> List[str]:
        """Represent a VBoxManageCommand as a list of terms.

        Returns:
            List[str]: command terms
        """
        return super().__repr__() + dict.__repr__(self._options)

    def __eq__(self, __o: List[str]) -> bool:
        """Equality of VBoxManageDirective.

        True when __o exactly starts with self._cmd
        and ends with self._options according to self._options_order.

        Args:
            __o (List[str]): list to compare

        Returns:
            bool: True if the VBoxManageDirective has the same
                  ordered terms and options than {__o} else False.
        """
        cmd_length = len(self._cmd)
        o_cmd, o_options = __o[:cmd_length], __o[cmd_length:]
        check_cmd = super().__eq__(o_cmd)
        check_options = []
        for flag in self._options_order:
            # extract flag from options
            check_options.append(o_options.pop(0) == flag)
            if not isinstance(self._options[flag], bool):
                # extract value from options
                check_options.append(o_options.pop(0) == str(self._options[flag]))
        check_options_length = len(__o[cmd_length:]) == len(check_options)
        return check_cmd and all(check_options) and check_options_length
