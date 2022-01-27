
trap kill_web_server SIGHUP SIGINT SIGKILL

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
    uvicorn main:app --reload
}

if [[ $1 == "docker" ]]
then
    if [[ $2 == 'rm' ]]
    then
        sudo docker rm -f api-1 && sudo docker image rm api_vbox:latest
    else
        sudo docker build -t api_vbox:latest . && sudo docker run -d --name api-1 -p 8080:80 api_vbox:latest 
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
