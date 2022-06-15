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
API_VBOX_HOST="0.0.0.0"
API_VBOX_PORT="8080"
API_VBOX_EXECMODE="container"
# Storage for API vbox
STORAGE_VMS_BASEFOLDER="media/kidr/RDD/vms/"
STORAGE_OVF_BASEFOLDER="/media/kidr/RDD/Documents/"
# RabbitMQ broker variables
RABBITMQ_HOST="0.0.0.0"
RABBITMQ_PORT="5672"
API_VBOX_USERS_REQUEST_QUEUE="api_vbox.users.request_queue"
# API authentication
API_AUTH_URL="http://localhost:8000"
APP_ENVIRONMENT="dev"
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

## Tests

Get a token bearer from `api_auth`
```bash
curl -XPOST http://localhost:8000/user/login -H "Content-Type: application/json" -d '{"email": "shihan@dojo.dev", "password": "shihan"}'
curl -XPOST http://localhost:8000/user/login -H "Content-Type: application/json" -d '{"email": "t.api_vbox.scope_3@dojo.dev", "password": "dojotest"}'
```

Use `/list` with token bearer
```bash
curl "http://localhost:8080/list?q=vms" -H "Authorization: Bearer "
```

Use `/import` with token bearer

```bash
curl -XPOST "http://localhost:8080/import" -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Im5hbWUiOiJzaGloYW4iLCJ1c2VySWQiOjJ9LCJyb2xlcyI6InNlbnNlaSIsInNjb3BlIjoiYXBpX3Zib3g6Y29udHJvbCBhcGlfdmJveDpjcmVhdGUgYXBpX3Zib3g6cmVhZCIsImlhdCI6MTY0OTMyNjE4NywiZXhwIjoxNjQ5MzI5Nzg3LCJpc3MiOiJhcGlfYXV0aCIsInN1YiI6IjIifQ.R8h4JnnN8ogWaO3WSDqeS2I1iW2f4zTWl5o-5WN9U2w" -d '{"vmname": "error-vm", "image": "pmint_box_dev.ova"}'
```