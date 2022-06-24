# DojoPlateforme

@author Rxinui
@administrator Rxinui sjosset

Please follow the directives written in this document.

## Project Management

- [JIRA project](https://kidr.atlassian.net/jira/software/projects/PFE/)
- [Github project](https://github.com/Rxinui/DojoPlateforme)
## Requirements

### System

    - Bash >=5.0.17
    - Docker >=20.10.7
    - docker-compose >=1.29.2
    - Python 3.9.10

### API `api_auth`

    - Node v16.14.0

### API `api_vbox`

    - VBoxManage 6.1.32_Ubuntur149290
## Installation

1. Clone the project repository

```shell
git clone https://github.com/Rxinui/DojoPlateforme.git
cd ./DojoPlateforme/ # move to project directory
```

2. Create an `.env` file which contains at least

```ini
API_AUTH_JWT_SECRET=vrGDkzLC0SLI8Rn7moDb
API_DB_PASSWORD=sifu
RPORTD_AUTH_PASSWORD=shihan
```

*Note: all environments variables declared inside `docker-compose.yml` file can be overrided by the `.env` file* 

3. Initialize DojoPlateforme's requirements on your system

```bash
# Run it with the wanted user.
# Check if the wanted user has all the necessary permissions.
./setup.sh init
```

4. Start DojoPlateforme

```bash
./setup.sh start
```

5. See more `setup.sh` options

```bash
./setup.sh -h
# to get more details about an action do as follow: ./setup.sh <action> -h
# example: ./setup.sh status -h
```