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
    uvicorn main:app --host localhost --port 8081 --reload 
}

if [[ $1 == "uvicorn" ]]
then
    run_web_server
    procs[0]=$!
    while :
    do
        sleep 60
    done
fi
