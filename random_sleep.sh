#!/bin/bash

if ! test $# -eq 1 ; then
    echo "Usage: random_sleep.sh <minutes>"
    exit
fi

# add 1 to allow modulus to reach {minutes}
# also prevents division by zero
sleep $(( (RANDOM%($1+1))*60 ))

