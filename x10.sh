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
command=${2^^} # force to upper case

# error check the input
if [[ ! "ON|OFF|DIM" =~ $command ]] ; then
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
code=${module:1} # not used, but here just in case

# ---------- locking and logging ----------

# include the bash mutex
. ./bashlock.sh

# try to acquire the lock X10 lock
if ! lock ~/locks/x10 ; then
	echo "failed to acquire lock, aborting X10 action: $@" 1>&2
	exit 1
fi

# for logging
echo $(date) "-- X10 $@"

# ------------- run command -------------

if [ $command = "DIM" ] ; then

    # make sure we got a third arg for DIMLEVEL
    if [ $# -ne 3 ] ; then
        help
        exit 0
    fi

    # DIM commands actually take 2 commands. One to select
    # the module, and the other to do the dimming
    br $module OFF $br_port
    br --house=$house --dim=$3 $house DIM $br_port
else
    # normal ON/OFF
    # run each command multiple times to ensure successful transmission
    # ugly, but helps...
    for i in seq $repeat
    do
        br $module $command $br_port
        sleep $repeat_wait
    done
fi

# ---------------- unlock ----------------
unlock ~/locks/x10
