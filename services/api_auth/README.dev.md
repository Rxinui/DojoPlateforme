# API Auth

@author Rxinui

For devs only.

## Installation

Based on **NodeJS v16.13.2** .

```shell
npm i
```

## Environments

Create a `.env` file

```shell
API_AUTH_HOST="localhost"
API_AUTH_PORT="80"
API_DB_HOST="0.0.0.0"
API_DB_USER="sifu"
API_DB_PASSWORD="sifu"
API_DB_DATABASE="dojo"
API_DB_CONNECTION_LIMIT=10
```

## Scopes

**Must keep this update, they rely on `db_dojo`**

- `api_vbox:control`: allows to use `start`, `stop`, `pause` a VM.
- `api_vbox:read`: allows to use all directives that read information `list`, `hostinfo`, ...
- `api_vbox:create`: allows to create a new VM instance by using `import` directive. 

## Tests

Login

```bash
curl -XPOST http://localhost:8000/user/login -H "Content-Type: application/json" -d '{"email": "admin@dojo.dev", "password": "admin"}'
```

Signup

```bash
curl -XPOST http://localhost:8000/user/new -H "Content-Type: application/json" -d '{"email": "admin@dojo1.dev", "password": "admin", "username": "admin"}'
```

Access protected resource `/profile`

**Note**: Bearer value **must not** be encapsulated by double quoute `"`.

```bash
curl localhost:8000/user/profile -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Im5hbWUiOiJhZG1pbiIsInVzZXJJZCI6MX0sInJvbGVzIjoiZGVzaGkgc2Vuc2VpIiwic2NvcGUiOiJhcGlfdmJveDphbGwiLCJpYXQiOjE2NDgwMzczNzAsImV4cCI6MTY0ODAzNzk3MCwiaXNzIjoiYXBpX2F1dGgiLCJzdWIiOiIxIn0.JNM_q_ENZjWKpsRMwVk_oUVeJvLqIUJUAZIe7aG3CTc"

curl localhost:8000/token/internal/verify -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Im5hbWUiOiJhZG1pbiIsInVzZXJJZCI6MX0sInJvbGVzIjoiZGVzaGkgc2Vuc2VpIiwic2NvcGUiOiJhcGlfdmJveDphbGwiLCJpYXQiOjE2NDc5OTAyODIsImV4cCI6MTY0Nzk5MDg4MiwiaXNzIjoiYXBpX2F1dGgiLCJzdWIiOiIxIn0.auKDX6mM7Nec5BjpxJ7MlgqPEqxXBhv0YqQ5fSn0ey0"
```