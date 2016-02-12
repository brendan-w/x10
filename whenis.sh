#!/bin/bash

# $X10_LAT and $X10_LNG
. ./location.sh


if [ "$#" -ne 1 ]; then
    echo "Usage:"
    echo "    whenis dusk"
    echo "    whenis dawn"
    exit 1
fi

DATA=`sunwait -p $X10_LAT $X10_LNG`

if test "$1" = "dawn"; then
    echo $DATA | sed --regexp-extended "s/.* Sun rises ([0-9]{2})([0-9]{2}) .*/\1:\2/"
elif test "$1" = "dusk"; then
    echo $DATA | sed --regexp-extended "s/.* sets ([0-9]{2})([0-9]{2}) .*/\1:\2/"
fi
