#!/bin/bash
# wait-for-it.sh - Script para esperar que un servicio esté disponible

TIMEOUT=15
QUIET=0

usage() {
    cat << USAGE >&2
Usage:
    $0 host:port [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
    -t TIMEOUT | --timeout=TIMEOUT
                                Timeout in seconds, zero for no timeout
    -q | --quiet                Don't output any status messages
    -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
    exit 1
}

wait_for() {
    local host=$1
    local port=$2
    local timeout=$3
    
    echo "Waiting for $host:$port..."
    
    local start_ts=$(date +%s)
    while :; do
        nc -z "$host" "$port" >/dev/null 2>&1
        local result=$?
        if [[ $result -eq 0 ]]; then
            local end_ts=$(date +%s)
            echo "$host:$port is available after $((end_ts - start_ts)) seconds"
            break
        fi
        
        if [[ $timeout -ne 0 ]]; then
            local current_ts=$(date +%s)
            if [[ $((current_ts - start_ts)) -gt $timeout ]]; then
                echo "Timeout occurred after waiting $timeout seconds for $host:$port"
                exit 1
            fi
        fi
        
        sleep 1
    done
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h)
            HOST="$2"
            shift 2
            ;;
        --host=*)
            HOST="${1#*=}"
            shift
            ;;
        -p)
            PORT="$2"
            shift 2
            ;;
        --port=*)
            PORT="${1#*=}"
            shift
            ;;
        -t)
            TIMEOUT="$2"
            shift 2
            ;;
        --timeout=*)
            TIMEOUT="${1#*=}"
            shift
            ;;
        -q | --quiet)
            QUIET=1
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            if [[ -z $HOST && -z $PORT ]]; then
                IFS=':' read -r HOST PORT <<< "$1"
            fi
            shift
            ;;
    esac
done

if [[ -z $HOST || -z $PORT ]]; then
    echo "Error: You need to provide a host and port to test."
    usage
fi

wait_for "$HOST" "$PORT" "$TIMEOUT"

if [[ $# -gt 0 ]]; then
    exec "$@"
fi
