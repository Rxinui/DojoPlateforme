#!/bin/bash

if [[ $1 == "build" ]]
then
    docker-compose up --build --force-recreate -V
elif [[ $1 == "up" ]]
then
    docker-compose up --force-recreate -V -d
elif [[ $1 == "down" ]]
then
    docker-compose down
fi