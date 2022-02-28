#!/bin/bash
"""
@author Rxinui
@date 2022-02-23

Install required linux dependencies.

Dependencies: (Please keep this list update)
- VBoxManage: VirtualBox CLI to manage .ova file
"""
echo -- Install linux dependencies --
echo + Install utils dependencies
sudo apt install wget curl
echo + Install Virtualbox dependency
sudo apt install linux-headers-azure virtualbox
# sudo apt install linux-headers-azure virtualbox virtualbox-ext-pack virtualbox-guest-additions-iso 
echo Check VBoxManage version
[[ 6.1.26_Ubuntur145957 == `VBoxManage --version` ]] || exit 1
echo + Set up the system/virtualbox/ folder
mkdir -p ./system/virtualbox/ovf ./system/virtualbox/vms