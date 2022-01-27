****# Cheatsheet Virtualbox

## VBoxManage

Manipulate `virtualbox` with command-line.

### `VBoxManage list`

Display information formatted as a list (`-s` sorted | `l` long information)

- display VMs: `VBoxManage list -s vms` 
- display running VMs: `VBoxManage list -s runningvms` 

### `VBoxManage import`

Import a virtualbox appliance (.ova, .ovf) and create a new VM from it

- display appliance information: `VBoxManage import <path_appliance> -n`
- create a new VM from appliance: `VBoxManage import <path_appliance> --vsys <int:vsys_number> [ --vmname <name> --basefolder <path_vms_storage> --options (keepnatmacs | keepallmacs) ]`

### `VBoxManage unregistervm`

Unregister a vm or delete it

- unregister a vm without deleting files: `VBoxManage unregistervm <vmname>`
- delete vm and its files: `VBoxManage unregistervm <vmname> --delete`

### `VBoxManage startvm`

Start a VM

- with GUI `VBoxManage startvm (<uuid> | <vmname>)`
- without GUI (remote) `VBoxManage startvm (<uuid> | <vmname>) --type headless`

### `VBoxManage controlvm`

Control vm to apply action such as

- Pause vm `VBoxManage controlvm (<uuid> | <vmname>) pause`
- Unpause vm `VBoxManage controlvm (<uuid> | <vmname>) resume`
- Power off vm `VBoxManage controlvm (<uuid> | <vmname>) poweroff`
- Save vm state then close `VBoxManage controlvm (<uuid> | <vmname>) savestate`
- Reboot vm without saving `VBoxManage controlvm (<uuid> | <vmname>) reset`