#!/bin/bash

usage () {
cat << EOF
Script to run suitable command during development phase.

@author Rxinui
@date 2022-03-01

Commands: (Please keep this update)
- docker: build an image and create an instance of it
- docker rm: remove container instance and its image
- uvicorn: run API webserver in development mode
EOF
}

trap kill_web_server SIGHUP SIGINT SIGKILL
source ./.env
api_image_tag="rxinui/api_vbox:latest"
api_container="api_vbox-1"
api_localport="8080"

function kill_web_server(){
    echo "Killing WEB server..."
    for i in `seq ${#procs[*]}`
    do
        e=$((i - 1))
        kill ${procs[$e]}
        echo "Server PID=${procs[$e]} killed."
    done
    exit 0
}

function run_web_server(){
    uvicorn main:app --host $API_VBOX_HOST --port $API_VBOX_PORT --reload 
}

if [[ $1 == "docker" ]]
then
    if [[ $2 == 'up' ]]
    then
        sudo docker-compose down -v --remove-orphans && sudo docker-compose up --build -V
    elif [[ $2 == 'rm' ]]
    then
        sudo docker rm -f $api_container && sudo docker image rm $api_image_tag
    else
        sudo docker build --rm -t $api_image_tag . && sudo docker run -d --name $api_container -p $api_localport:80 $api_image_tag 
    fi
elif [[ $1 == "uvicorn" ]]
then
    run_web_server
    procs[0]=$!
    while :
    do
        sleep 60
    done
fi
