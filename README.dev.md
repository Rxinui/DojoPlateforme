# Project PFE

@author Rxinui
@administrator Rxinui sjosset

Please follow the directives written in this document.

## Project Management

- [JIRA project](https://kidr.atlassian.net/jira/software/projects/PFE/)
- [Github project](https://github.com/Rxinui/DojoPlateforme)

## Installation

**Attention: Working on ns343000 server is reserved only for @administrator**

Developers must work on their localhost machine.

### Requirements

#### API api_vbox

- Python 3.9.10

### Replicate a production-like env

1. Clone the source code

```shell
# ssh: git clone git@github.com:Rxinui/DojoPlateforme.git
git clone https://github.com/Rxinui/DojoPlateforme.git # https
cd ./DojoPlateforme/ # move to project directory
```

2. Install virtualenv

Required Python 3.9.10 virtual env

```shell
python3.9 -m pip install virtualenv # install venv
python3.9 -m venv pyvenv # create pyvenv
source ./pyvenv/bin/activate # run the virtualenv
python -m pip install -r requirements.txt # install dependencies
```

3. Configure synchronisation

Create a hidden configuration file named `.sync.client.json` within the project root to synchronise your machine with the production server.

```jsonc
{
    "server": {
        "syncConfPath": "/opt/pfe/.sync.server.json" // production server conf path [do not change]
    },
    "client": {
        "sshConfPath": "<ssh_configfile_path>",
        "sshHost": "<ssh_host_in_configfile>",
        "sshPrivateKeyPath": "<ssh_private_key>" // Optional
    }
}
```

4. Run synchronisation with production

Run the synchronisation file `sync.dev.py` **with pyvenv**.

```shell
python sync.dev.py
```

Now you have in your localhost machine a production-like environment.
