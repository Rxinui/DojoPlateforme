#!/bin/bash

########## setup.sh ##########
# Initialize an environment to meet the requirements with DojoPlateforme.
#
# Usage:
#   sudo ./setup.sh <action> [ACTION_OPTIONS]
#
# Options:
#
# @author Rxinui
##############################

########## Environments ##########

# Load and export environments vars from .env file
set -a && . ./.env && set +a

##################################

########## Functions ##########

##
# Execute command as sudo user.
#
# Paramters:
#   $1: command to execute between single quote (ie. '<command>')
##
sudoexec() {
    sudo /bin/bash -c "$1"
}

##
# Log an information message.
#
# Parameters:
#   $1: info message to log.
##
log_info() {
    echo -e "\e[36mINFO: $1\e[0m"
}

##
# Log an error message.
#
# Parameters:
#   $1: error message to log.
##
log_error() {
    echo -e "\e[31mERROR: $1\e[0m"
}

##
# Generate a random secret which is alphanumerical without special chars
#
# Usage:
#   generate_random_secret [length]
#
# Parameters:
#   $1: length of secrets. Default to 20 chars.
##
generate_random_secret() {
    _length=$1
    if [[ -z $_length ]]; then
        _length=20
    fi
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w$_length | head -n 1
}

##
# Replace secret in a variable by a random generated secret.
# It will perform a search/replace action into a variable according to
# its name pattern within in a given file.
#
# Usage:
#   search_replace_secret <filepath> <var_pattern> [<var_pattern_2> ...]
#
# Parameters:
#   $1: [Required] File where the search replace will be executed.
#   $2: [Required] Variable pattern name to search.
#   $N: Other variable pattern name to search.
##
search_replace_secret() {
    _file=$1
    shift
    if [[ -z $_file ]]; then
        log_error "Missing required positional parameter <filepath>."
        exit -1
    fi
    if [[ $# -eq 0 ]]; then
        log_error "Missing required positional parameter <variable_pattern>."
        exit -1
    fi
    # Replace the value by newly generated secret
    for _varpattern; do
        _newsecret=$(generate_random_secret)
        sed_pattern+="s/(${_varpattern})(=)(\"?.*\"?)/\1\2${_newsecret}/g;"
        _logmsg+="\n\t$_varpattern"
    done
    sed -E -i $sed_pattern $_file
    log_info "Replace following (possible) secrets in '$_file':$_logmsg"
}
###############################

########## Programs ##########

##
# Command 'secret' performs various manipulations on secrets (ie. password, token)
#
# Options:
#   reload, generate: generate new secrets within project ./.env file.
##
action_secret() {
    case $1 in
    "generate" | "reload")
        _envfile="./.env"
        if [[ ! -f $_envfile ]]; then
            log_error "Missing global ./.env file"
            exit 1
        fi
        _to_force="y"
        if [[ $2 != "-f" && $2 != "--force" ]]; then
            read -p "Are you sure you want to reload secrets? It will [y/n]? " _to_force
        fi
        if [[ $_to_force == "y" || $_to_force == "Y" ]]; then
            log_info "Updating '$_envfile' secrets..."
            search_replace_secret $_envfile API_AUTH_JWT_SECRET
            log_info "Done."
        fi
        ;;
    *)
        help_action_secret
        ;;
    esac
}

##
# Command 'start' performs action to run docker services
##
action_start() {
    log_info "Starting docker services..."
    case $1 in
    "-h" | "--help")
        help_action_start
        ;;
    "--build")
        docker-compose up -d -V --force-recreate --build
        ;;
    *)
        docker-compose up -d -V --force-recreate
        ;;
    esac
}

##
# Command 'start' performs action to stop docker services
##
action_stop() {
    log_info "Stopping docker services..."
    docker-compose down -v --remove-orphans
}

##
# Command 'init' performs action to initialize requirements such as default directories
#
# Creates:
#   - Storage VMS basefolder
#   - Storage .ovf images basefolder
#
##
action_init() {
    log_info "Initializing DojoPlateforme..."
    # Linux/Unix packages and dependencies #
    action_check packages
    if [[ $? -ne 0 ]]; then
        log_error "Missing linux packages and dependencies"
        exit 2
    fi
    which virtualenv >/dev/null
    if [[ $? -eq 0 ]]; then
        _to_venv="y"
        read -p "Install python3.9 dependencies inside a virtualenv? [y/n] " _to_venv
        if [[ $_to_venv == "y" || $_to_venv == "Y" ]]; then
            log_info "Installing within pyvenv/ ..."
            python3 -m venv pyvenv                     # create pyvenv
            source ./pyvenv/bin/activate               # run the virtualenv
            python3 -m pip install --upgrade pip       # install dependencies
            python3 -m pip install -r requirements.txt # install dependencies
        fi
    fi
    if [[ -z $_to_venv || $_to_venv == "n" || $_to_venv == "N" ]]; then
        log_info "Installing within global python libraries..."
        python3 -m pip install -r requirements.txt # install dependencies
    fi
    # Directories and files #
    log_info "Creating storage vms basefolder"
    sudoexec "mkdir -m 755 -p ${STORAGE_VMS_BASEFOLDER}"
    log_info "Creating storage .ovf images basefolder"
    sudoexec "mkdir -m 755 -p ${STORAGE_OVF_BASEFOLDER}"
    log_info "Creating system binaries folder"
    mkdir -m 755 -p ${PWD}/bin/
    log_info "Importing binaries script to binaries folder"
    api_vbox_request_path="$PWD/bin/api_vbox_request"
    ln -sf "$PWD/services/api_vbox/scripts/rabbitmq_server.py" $api_vbox_request_path
    sudoexec "chmod 755 $api_vbox_request_path"
    sed -E -i "1 i\#!$(which python3)" $api_vbox_request_path
    action_secret reload
}

##
# Command 'status' performs status check on given services
#
# Parameters:
#   $1: service's name. If empty then display all services status.
#
# Options:
#   --running: display services that are running.
#   --exited: display services that are exited.
#
##
action_status() {
    log_info "Status services..."
    _cmd_status="docker ps -a"
    while [[ $# -ne 0 ]]; do
        case $1 in
        "-h" | "--help")
            help_action_status
            ;;
        "--exited")
            _cmd_status+=' -f "status=exited"'
            ;;
        "--running")
            _cmd_status+=' -f "status=running"'
            ;;
        *) # filter by name
            _cmd_status+=" -f \"name=$1\""
            ;;
        esac
        shift
    done
    sudoexec "$_cmd_status"
}

##
# Command 'check' performs verification to check requirements and services states
##
action_check() {
    _h2() {
        echo -e -n "    $1:"
    }
    _ok() {
        echo -e " \e[1m\e[32mOK\e[0m"
    }
    _ko() {
        echo -e " \e[1m\e[33mKO\e[0m"
    }
    subaction_check() {
        declare -i check_code=0
        case $1 in
        "-h" | "--help")
            help_action_check
            ;;
        "packages" | "dependencies")
            log_info "Linux/Unix packages and dependencies"
            _h2 "python3.9"
            which python3 >/dev/null
            if [[ $? -eq 0 && $(python3 --version) == *"3.9."* ]]; then
                _ok
            else
                _ko && ((check_code++))
            fi
            _h2 "pip3"
            (which pip3 >/dev/null) && [[ $? -eq 0 ]] && _ok || _ko
            _h2 "virtualenv"
            (which virtualenv >/dev/null) && [[ $? -eq 0 ]] && _ok || _ko
            _h2 "docker"
            (which docker >/dev/null) && [[ $? -eq 0 ]] && _ok || _ko
            _h2 "docker-compose"
            (which docker-compose >/dev/null) && [[ $? -eq 0 ]] && _ok || _ko
            _h2 "curl"
            (which curl >/dev/null) && [[ $? -eq 0 ]] && _ok || _ko
            _h2 "VBoxManage"
            (which curl >/dev/null) && [[ $? -eq 0 ]] && _ok || _ko
            return $check_code
            ;;
        "directories" | "files")
            log_info "Directories and files"
            _h2 "Directory for STORAGE_OVF_BASEFOLDER"
            [[ -d $STORAGE_OVF_BASEFOLDER ]] && _ok || _ko
            _h2 "Directory for STORAGE_VMS_BASEFOLDER"
            [[ -d $STORAGE_VMS_BASEFOLDER ]] && _ok || _ko
            _h2 "Directory for project's binaries"
            [[ -d $PWD/bin/ ]] && _ok || _ko
            _h2 "DojoPlateforme's root project .env file"
            [[ -f $PWD/.env ]] && _ok || _ko
            return $check_code
            ;;
        *)
            subaction_check packages
            ((check_code = $?))
            subaction_check directories
            ((check_code += $?))
            return $check_code
            ;;
        esac
    }
    log_info "Checking DojoPlateforme's requirements..."
    subaction_check $1
}

##
# Command 'uninstall' remove each dependencies of DojoPlateforme
##
action_uninstall() {
    log_info "Uninstall dependencies..."
    if [[ ! -d "$PWD/pyvenv/" ]]; then
        log_info "Removing python3.9 dependencies registered in requirements.txt..."
        pip3 uninstall -r requirements.txt -y
    else
        log_info "Removing python3.9 virtualenv pyvenv/..."
        sudo rm -rf $PWD/pyvenv/
    fi
    sudo rm -rf $STORAGE_OVF_BASEFOLDER $STORAGE_VMS_BASEFOLDER $PWD/bin/
}

main() {
    case $1 in
    "check")
        shift
        action_check $@
        ;;
    "init")
        shift
        action_init $@
        ;;
    "start")
        shift
        action_start $@
        ;;
    "status")
        shift
        action_status $@
        ;;
    "stop")
        shift
        action_stop $@
        ;;
    "secret")
        shift
        action_secret $@
        ;;
    "uninstall")
        shift
        action_uninstall $@
        ;;
    *)
        help_main
        ;;
    esac
    exit $?
}
##############################

########## Helps ##########
help_main() {
    cat <<EOF
./setup.sh: Setup the machine to run DojoPlateforme.

Usage: sudo ./setup.sh <action> [ACTION_OPTIONS]

Various actions are available.

Actions:
    check       Verify services status and initializiation status
    init        Initialize machine to run DojoPlateforme
    secret      Perform action in relation with secrets
    start       Start DojoPlateforme's services
    status      Check status of DojoPlateforme's services
    stop        Stop DojoPlateforme's services
    uninstall   Remove each dependencies of DojoPlateforme

ACTIONS_OPTIONS are case-sensitive.
EOF
}

help_action_status() {
    cat <<EOF
./setup.sh status: Check status of DojoPlateforme's services

Usage: sudo ./setup.sh status [ACTION_OPTIONS]

Various actions are available.

    [Options]
    --exited        Show exited services
    --running       Show running services

ACTIONS_OPTIONS are case-sensitive.
EOF
}

help_action_check() {
    cat <<EOF
./setup.sh check: Verify services status and initializiation status

Usage: sudo ./setup.sh check [ACTION_OPTIONS]

Various actions are available.

Actions:
    packages, dependencies      Check required Linux/Unix packages
    directories, files          Check required directories and files

ACTIONS_OPTIONS are case-sensitive.
EOF
}

help_action_secret() {
    cat <<EOF
./setup.sh secret: Perform action in relation with secrets

Usage: sudo ./setup.sh secret [ACTION_OPTIONS]

Various actions are available.

Actions:
    reload, generate        Generate new secrets within "./.env" file
        [Options]
        -f, --force         Force generation of secrets

ACTIONS_OPTIONS are case-sensitive.
EOF
}

help_action_start() {
    cat <<EOF
./setup.sh start: Start DojoPlateforme's services

Usage: sudo ./setup.sh start [ACTION_OPTIONS]

Various actions are available.

    [Options]
    --build     Build services from its Dockerfile (source)

ACTIONS_OPTIONS are case-sensitive.
EOF
}

###########################

########## Main program ##########
main $@
exit 0
