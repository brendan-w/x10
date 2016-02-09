#!/bin/bash

SCHED=./sched.x10

nano -Y sh $SCHED && ./compile_crontab.py $SCHED > sched.crontab && crontab sched.crontab