#!/bin/bash

# global settings
br_port="--port=/dev/ttyUSB0"
repeat=3
repeat_wait=15

help() {
    # print the intro text with command samples
    cat /etc/motd
    echo "x10 command usage:"
    echo "    x10 MODULE COMMAND [DIMLEVEL]"
    echo ""
    echo "    MODULE:   C5"
    echo "    COMMAND:  ON, OFF, DIM"
    echo "    DIMLEVEL: a number between -12 and 12"
    echo ""
}

# if there are no arguments, show help
if [ $# -lt 2 ] ; then
    help
    exit 0
fi

module=$1
command=$2

# error check the input
if [[ ! "ON|OFF|DIM" =~ ${command^^} ]] ; then
    echo "Invalid command: $2" 1>&2
    help
    exit 0
fi

if [ ${#module} -lt 2 ] ; then
    echo "Invalid module code: $1" 1>&2
    help
    exit 0
fi

house=${module:0:1}
code=${module:1}

# include the bash mutex
. ./bashlock.sh

# try to acquire the lock X10 lock
if ! lock ~/locks/x10 ; then
	echo "failed to acquire lock, aborting X10 action: $@" 1>&2
	exit 1
fi

# for logging
echo $(date) "-- X10 $@"

# ---------- run command ----------

# run each command multiple times to ensure successful transmission
# ugly, but helps...
for i in seq $repeat
do
    br $@ $br_port
    sleep $repeat_wait
done

# release our lock
unlock ~/locks/x10
