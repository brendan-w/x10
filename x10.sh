#!/bin/bash

# if there are no arguments, show help
if test $# -eq 0
then
    # print the intro text with command samples
    cat /etc/motd
    echo "x10 command usage:"
    echo "    x10 MODULE COMMAND [DIMLEVEL]"
    echo ""
    echo "    MODULE: C5"
    echo "    COMMAND: ON, OFF, DIM"
    echo "    DIMLEVEL: a number between -12 and 12"
    echo ""
    exit 0
fi


# include the bash mutex
. ./bashlock.sh

# try to acquire the lock X10 lock
if ! lock ~/locks/x10 ; then
	echo "failed to acquire lock, aborting X10 action: $@" 1>&2
	exit 1
fi

echo $(date) "-- X10 $@"

# run each command multiple times to ensure successful transmission
# ugly, but helps...
for i in seq 3
do
    br $@ --port=/dev/ttyUSB0
    sleep 15
done

# release our lock
unlock ~/locks/x10
