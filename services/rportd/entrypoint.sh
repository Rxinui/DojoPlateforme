#!/bin/bash
##
# Docker entrypoint to start:
# - rportd: rport service
# - lighttpd: small web static content server that stores rportd files require by rport-client (ie. fingerprint)
#
# @author Rxinui
##

_log(){
    echo "$(date +'%F %T') $0> $1"
}

set -e
_log "Starting rportd"
rportd -c /etc/rport/rportd.conf --log-level info &
path_fingerprint="/var/lib/rport/rportd-fingerprint.txt"
if [[ ! -f $path_fingerprint ]]; then
    sleep 3
fi
install -m 775 -g rport $path_fingerprint "/var/lib/rport/docroot/fingerprint.txt"
_log "Fingerprint is now available"
tail -f /dev/null