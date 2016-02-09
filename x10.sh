#!/bin/bash

# if there are no arguments, show help
if test $# -eq 0
then
    # print the intro text with command samples
    cat /etc/motd
    echo "for  details on the x10 command itself, type: br --help"
    echo ""
    exit 0
fi


# include the bash mutex
. ./bashlock.sh

# try to acquire the lock X10 lock
lock ~/locks/x10

echo $(date) "-- X10 $@" >> ~/x10.log

# run each command 
for i in seq 3
do
    br $@ --port=/dev/ttyUSB0 >> x10.log 2>&1
    sleep 5
done

# release our lock
unlock ~/locks/x10
