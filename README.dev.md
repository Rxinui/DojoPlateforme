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

#### API api_auth

- Node v16.14.0

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