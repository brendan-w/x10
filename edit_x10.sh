#!/bin/bash

# the default schedule file
SCHEDULE=~/schedule.x10
TMP_CRONTAB=/tmp/x10.crontab

# or, if the user specified a schedule file
if [ "$#" -e 1 ]; then
    SCHEDULE="$1"
fi


# let the user edit the schedule
nano -Y sh $SCHEDULE

# compile and write the X10 crontab
./compile_crontab.py $SCHEDULE | cat ./header.crontab - > $TMP_CRONTAB

# load our crontab, and delete the temporary file
crontab $TMP_CRONTAB
rm $TMP_CRONTAB
