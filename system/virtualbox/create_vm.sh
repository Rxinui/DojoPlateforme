#!/bin/bash

"""
Create a virtualbox VM

@state: wip; ko
@version: 0.0.1
@author: rly
"""

path_ovf=$1
vmname=$2
basefolder=$3

create_vm() {
  VBoxManage import $path_ovf --vsys 0 --vmname $vmname --basefolder $3 --options keepnatmacs;
}

main() {
  create_vm;
}

main "$@";