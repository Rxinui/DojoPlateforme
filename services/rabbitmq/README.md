# RabbitMQ service

@author Rxinui

RabbitMQ service is used to manage messages from our different services.
Below, a [list of services that require RabbitMQ](##Services-using-RabbitMQ) with the pattern used.

## Configuration

// To define

## Services using RabbitMQ 

### API Vbox

The pattern used is **RPC**. API Vbox aims to be containerized on a Docker container. Therefore, it is not possible for the API to execute a `VBoxManage` command-line. It is necessary to forward the execution of the `VBoxManage` commands to the production server. To do so, RabbitMQ broker with the RPC pattern allow a request-reply exchange with queues.

An overview can be represented as follow:

![RabbitMQ broker used by API Vbox](https://drive.google.com/file/d/1DAu51tWIBtBgt2b3ZpO4dJtkBB7UNSRj/view?usp=sharing)


