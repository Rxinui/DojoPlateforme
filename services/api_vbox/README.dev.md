# API vbox

@author Rxinui

For devs only.

## Requirements

This API is a wrapper of `VBoxManage` command-line. Therefore, VirtualBox 6.1 package must be installed on the host machine.

### Environment file `.env`

- `API_VBOX_HOST`: container host. Default to 0.0.0.0
- `API_VBOX_PORT`: container port. Default to 8080
- `API_VBOX_EXECMODE`: environment to execute processus. When the API receives a a request (ie. list), it calls the linux command `VBoxManage` that are in charge of the VirtualBox management. Therefore, it is requires for the API Vbox to be used on a machine where `VBoxManage` is installed. There are 2 options:
    - `local`: implies that API Vbox is running directly on a host machine where `VBoxManage` is correctly installed. Python will use the library `subprocess` to execute the commands
    - `container`: implies that API Vbox is running on a container (ie. Docker). The docker image is built on `python:3.9` image and does not have any way to install `VBoxManage` on the container. All the `VBoxManage` command will be redirected to the host machine and will expect a reply with the following output. The output will be transfer to the client by the API

Example:

```ini
API_VBOX_HOST="127.0.0.1"
API_VBOX_PORT="8080"
API_VBOX_EXECMODE="container"
# RabbitMQ broker variables
API_VBOX_RABBITMQ_HOST="0.0.0.0"
API_VBOX_RABBITMQ_PORT="5672"
API_VBOX_USERS_REQUEST_QUEUE="api_vbox.users.request_queue"
```

## FastAPI

Run the FastAPI server in classic development mode

```sh
uvicorn main:app --reload
```

or launch the `dev.sh` script (recommended)

```sh
./dev.sh uvicorn
```