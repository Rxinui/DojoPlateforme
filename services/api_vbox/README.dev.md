# API vbox

@author Rxinui

For devs only.

## Requirements

This API is a wrapper of `VBoxManage` command-line. Therefore, VirtualBox 6.1 package must be installed on the host machine.

.env file

```
API_VBOX_HOST="127.0.0.1"
API_VBOX_PORT="8080"
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