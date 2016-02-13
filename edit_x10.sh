#!/bin/bash

# the default schedule file
SCHEDULE=~/schedule.x10
TMP_CRONTAB=/tmp/x10.crontab

# or, if the user specified a schedule file
if test $# -eq 1 ; then
    SCHEDULE="$1"
fi


# let the user edit the schedule
nano -Y sh $SCHEDULE

# kill any lingering sunwaits, since they have probably been altered

# kill the cron line first
# if you only kill the sunwaits themselves, bash will
# move on and execute the X10 commands
pkill -f " -c sunwait" # the bash that cron spawned
pkill -f "sunwait" # the actual sunwaits

# compile and write the X10 crontab
./compile_crontab.py $SCHEDULE | cat ~/base.crontab ~/location.sh - > $TMP_CRONTAB

# load our crontab, and delete the temporary file
crontab $TMP_CRONTAB
rm $TMP_CRONTAB
