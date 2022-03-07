# RabbitMQ server for API Vbox

Requires a env file `.api_vbox.env` which can be obtained by creating a hard link from `services/api_vbox/.env` to this directory renamed as `.api_vbox.env`

Within this file, there are the required variables

```ini
API_VBOX_RABBITMQ_HOST="0.0.0.0"
API_VBOX_RABBITMQ_PORT="5672"
API_VBOX_USERS_REQUEST_QUEUE="api_vbox.users.request_queue"
```