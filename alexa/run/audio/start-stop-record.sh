#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$( dirname "$DIR" )"
source $PARENT/config

PID_FILE="/var/run/pt-pulse-record.pid"
PID=$(cat $PID_FILE 2>/dev/null)
TIMEOUT="${TIMEOUT:-15}"
PULSE_RECORD_SCRIPT="$DIR/helper/pt-pulse-record.py"

cleanup() {
    if [ -f "$AVS_REQ_FILE" ]; then
        sudo rm -f "$AVS_REQ_FILE"
    fi
}

start() {
    if kill -0 $PID &> /dev/null; then
        echo "already running"
    else
        echo "started"
        cleanup
        $PULSE_RECORD_SCRIPT &
        echo $! > $PID_FILE
    fi
}

stop() {
    if kill -0 $PID &> /dev/null; then
        kill -TERM $PID
        timeout &
        trap "trap - SIGTERM &>/dev/null && kill -KILL $! &>/dev/null" SIGINT SIGTERM EXIT
        wait_pid $PID
        echo "stopped"
        exit 0 
    else
        echo "not running"
    fi
}

timeout() {
    sleep $TIMEOUT
    if ! kill -0 $PID &> /dev/null; then
        exit 0
    else
        kill -KILL $PID
        sleep 1
        if ! kill -0 $PID &> /dev/null; then
            printf '%s\n' "Process timed out, and was terminated by SIGKILL."
            exit 2
        else
            printf '%s\n' "Process timed out, but can't be terminated (SIGKILL ineffective)."
            exit 1
        fi
    fi
}

wait_pid() {
    while [ -e /proc/$1 ]; do
        sleep .5
    done
}

$@
