"""
Python builder for VBoxManage 'list' subcommand-line tool.

@author rly
@date 21/01/2022
@see https://www.virtualbox.org/manual/ch08.html#vboxmanage-list
"""

import re
from typing import Dict, List, Tuple
from vboxmanage import VBoxManageCommand


class VBoxManageList(VBoxManageCommand):
    """Python wrapper for `VBoxManage list`."""

    ORIGIN = "list"

    @classmethod
    def __process(
        cls, directive: str, sort: bool = False, long: bool = False
    ) -> List[str]:
        """Build the list subcommand according to {cmd} parameter.

        Args:
            directive (str): list's directive to build
            sort (bool): add list sort option
            long (bool): add list long option that display in-depth information

        Returns:
            (str): list subcommand built
        """
        _cmd = [cls.CLI, cls.ORIGIN]
        if sort:
            _cmd.append("-s")
        if long:
            _cmd.append("-l")
        _cmd.append(directive)
        return _cmd

    @staticmethod
    def vms(sort: bool = False, long: bool = False) -> List[str]:
        """Specify 'vms' directive to list subcommand.

        Returns:
            (str): list vms command-line.
        """
        return VBoxManageList.__process("vms", sort, long)

    @staticmethod
    def runningvms(sort: bool = False, long: bool = False) -> List[str]:
        """Specify 'runningvms' directive to list subcommand.

        Returns:
            (str): list runningvms command-line.
        """
        return VBoxManageList.__process("runningvms", sort, long)

    @staticmethod
    def intnets(sort: bool = False, long: bool = False) -> List[str]:
        """Specify 'intnets' directive to list subcommand.

        Returns:
            (str): list intnets command-line.
        """
        return VBoxManageList.__process("intnets", sort, long)

    @staticmethod
    def hostinfo(sort: bool = False, long: bool = False) -> List[str]:
        """Specify 'hostinfo' directive to list subcommand.

        Returns:
            (str): list hostinfo command-line.
        """
        return VBoxManageList.__process("hostinfo", sort, long)

    @staticmethod
    def groups(sort: bool = False, long: bool = False) -> List[str]:
        """Specify 'groups' directive to list subcommand.

        Returns:
            (str): list groups command-line.
        """
        return VBoxManageList.__process("groups", sort, long)

    @staticmethod
    def systemproperties(sort: bool = False, long: bool = False) -> List[str]:
        """Specify 'systemproperties' directive to list subcommand.

        Returns:
            (str): list systemproperties command-line.
        """
        return VBoxManageList.__process("systemproperties", sort, long)

    @staticmethod
    def bridgedifs(sort: bool = False, long: bool = False) -> List[str]:
        """Specify 'bridgedifs' directive to list subcommand.

        Returns:
            (str): list bridgedifs command-line.
        """
        return VBoxManageList.__process("bridgedifs", sort, long)

    @staticmethod
    def hostonlyifs(sort: bool = False, long: bool = False) -> List[str]:
        """Specify 'hostonlyifs' directive to list subcommand.

        Returns:
            (str): list hostonlyifs command-line.
        """
        return VBoxManageList.__process("hostonlyifs", sort, long)

    @staticmethod
    def natnets(sort: bool = False, long: bool = False) -> List[str]:
        """Specify 'natnets' directive to list subcommand.

        Returns:
            (str): list natnets command-line.
        """
        return VBoxManageList.__process("natnets", sort, long)

    @staticmethod
    def dhcpservers(sort: bool = False, long: bool = False) -> List[str]:
        """Specify 'dhcpservers' directive to list subcommand.

        Returns:
            (str): list dhcpservers command-line.
        """
        return VBoxManageList.__process("dhcpservers", sort, long)


class VBoxManageListParser:
    """
    Parser for VBoxManageList command result.
    """

    @staticmethod
    def __parse_key_value(k: str, v: str) -> Tuple[str, str]:
        k = k.strip().lower().replace(" ", "_")  # replace whitespace as underscore
        k = re.sub(r"[)(,\.]", "", k)  # remove special chars
        return k, v.strip()

    @staticmethod
    def parse_vms(output: str, long: bool = False) -> Dict[str, str]:
        """
        Retrieve vbox name and vbox uuid from `VBoxManage list vms`.

        Args:
            output (str): output from command

        Returns:
            (Dict[str,str]): vbox id as key and vbox name as value of the dict
        """

        def parse_short_vms() -> Dict[str, str]:
            """
            Example:
                before: '"pmint_box_dev-1" {77bd1e0e-edc6-47fc-807a-987c296c64dd}'
                after: {"pmint_box_dev-1": "77bd1e0e-edc6-47fc-807a-987c296c64dd"}
            """
            get_vm = lambda l: re.search(r"\"([_\d\w-]+)\"\s+\{([\d\w-]+)\}", l.strip())
            vms = {}
            for line in output.splitlines():
                if line:
                    vm = get_vm(line)
                    vms[vm.group(2)] = vm.group(1)
            return vms

        def parse_long_vms() -> Dict[str, str]:
            sep_vm = "\n\n\n"
            vms = {}
            for vm_info in output.split(sep_vm):
                vm = {}
                if vm_info:
                    for info in vm_info.splitlines():
                        match = re.search(r"^([\d\w\s)(,-/]+):(.*)", info)
                        if match:
                            (
                                info_desc,
                                info_value,
                            ) = VBoxManageListParser.__parse_key_value(
                                match.group(1), match.group(2)
                            )
                            if (
                                info_value == "<none>"
                                or info_value == ""
                                or not info_value
                            ):
                                info_value = None
                            vm[info_desc] = info_value
                    vms[vm["uuid"]] = vm
            return vms

        return parse_long_vms() if long else parse_short_vms()

    @staticmethod
    def parse_runningvms(output: str, long: bool = False) -> Dict[str, str]:
        """
        Retrieve vbox name and vbox uuid from `VBoxManage list runningvms`.

        Example:
            before: '"pmint_box_dev-1" {77bd1e0e-edc6-47fc-807a-987c296c64dd}'
            after: {"pmint_box_dev-1": "77bd1e0e-edc6-47fc-807a-987c296c64dd"}

        Args:
            output (str): output from command

        Returns:
            (Dict[str,str]): vbox id as key and vbox name as value of the dict
        """
        return VBoxManageListParser.parse_vms(output, long)

    @staticmethod
    def parse_hostinfo(output: str, long: bool = False) -> Dict[str, str]:
        """
        Retrieve host info with vbox uuid or name from `VBoxManage list hostinfo`.

        Args:
            output (str): output from command
            long (bool): long hostinfo is the same as hostinfo

        Returns:
            (Dict[str,str]): vbox host info description as key and host info value as value
        """
        parsed = {}
        for line in output.splitlines()[2:]:
            info_desc, info_value = VBoxManageListParser.__parse_key_value(
                *line.split(": ")
            )
            parsed[info_desc] = info_value
        return parsed
