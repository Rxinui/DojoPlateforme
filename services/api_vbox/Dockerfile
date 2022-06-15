FROM python:3.9

WORKDIR /app

COPY ./ /app/
RUN python -m pip install pip --upgrade && \
    python -m pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV API_VBOX_HOST 0.0.0.0
ENV API_VBOX_PORT 80
ENV API_VBOX_EXECMODE="local"
ENV RABBITMQ_HOST="0.0.0.0"
ENV RABBITMQ_PORT="5672"
ENV API_VBOX_USERS_REQUEST_QUEUE="api_vbox.users.request_queue"

CMD ["bash","-c", "uvicorn main:app --port $API_VBOX_PORT --host $API_VBOX_HOST"]
