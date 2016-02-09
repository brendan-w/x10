#!/bin/env python3

"""
    This script converts custom X10 schedule files into crontab lines.
    Please refer to the sample schedule file for details.
"""


import os
import sys
import re
import datetime


DEFAULT_CRON_LINE = "{minute} {hour} * * * {sunwait} ; {random} ; {command}"

NULL_COMMAND = "true"
X10_COMMAND = "/home/x10/x10.sh"
SUNWAIT_COMMAND = "sunwait {args} $X10_LAT $X10_LNG"
RANDOM_COMMAND = "sleep $(( (RANDOM%{minutes})*60 ))"

COMMENT_CHAR = "#"
TIME_COMMAND_SEP = ";"
NEAR_FUTURE = 1 # minutes


# token classifiers
time_re = re.compile(r"\d+:\d+(am|pm)$")
astro_re = re.compile(r"dawn|dusk$")
offset_re = re.compile(r"[+\-]\d+$")
random_re = re.compile(r"~\d+$")



# returns iterable of letters from start to stop
# alphabet_region("a", "z") = ["a", "b", "c", ... "z"]
alphabet_region = lambda start, stop: map(chr, range(ord(start), ord(stop) + 1))




def parse_time(token):
    colon = token.index(":")
    hour = int(token[:colon])
    minute = int(token[colon+1:-2]) # -2 discards AM/PM

    if token.endswith("pm"):
        hour += 12

    return (hour, minute)


def time_add_minutes(time, minutes):
    m = time[1] + minutes
    h = time[0] + (m // 60)
    m = m % 60
    h = h % 24
    return (h, m)


def parse(line):
    """ Main parsing function """

    if TIME_COMMAND_SEP not in line:
        return None

    # get the position of the first seperator
    sep_pos = line.index(TIME_COMMAND_SEP)

    # split into the time and command portions
    # and strip off any leading/trailing spaces
    time_part = line[:sep_pos].strip()
    command_part = line[sep_pos+1:].strip()



    # parse the time part

    time_part = time_part.lower() # be case insensitive
    time_tokens = time_part.split() # tokenize by spaces


    time = None # (hour, minute) in military time
    astro = None
    offset = 0
    random_minutes = 0


    # parse each token
    for token in time_tokens:
        
        if time_re.match(token):
            time = parse_time(token)
        elif astro_re.match(token):
            astro = token
        elif offset_re.match(token):
            offset = int(token)
        elif random_re.match(token):
            random_minutes = int(token[1:])
        else:
            return None # encountered unknown token, halt


    # post-process the time stamp (and ensure it's there at all)

    if time and not astro:
        # if this is a hard coded time
        time = time_add_minutes(time, offset)
    elif astro and not time:
        # if this is an astronomical time
        # pick a time in the near future to activate the astronomical wait (sunwait)
        now = datetime.datetime.now().time()
        time = time_add_minutes((now.hour, now.minute), NEAR_FUTURE)
    elif time and astro:
        # leave it. This allows you to manually set the time that astro
        # waits (sunwaits) will begin
        pass
    else:
        return None # neither a time, or an astro were specified


    # build the parsed data into a cron line

    minute = time[1] # these should always be present
    hour = time[0]
    sunwait = NULL_COMMAND
    random = NULL_COMMAND
    command = X10_COMMAND + " " + command_part

    # prevent a division by zero in the random wait
    if random_minutes > 0:
        random = RANDOM_COMMAND.format(minutes=random_minutes)

    if astro:
        args = ""

        if   astro == "dawn": args += "sun up"
        elif astro == "dusk": args += "sun down"

        # use sunwait's offset facilities
        if offset:
            if offset > 0:
                t = time_add_minutes((0,0), offset)
                args += " +%02d:%02d" % t
            elif offset < 0:
                t = time_add_minutes((0,0), -offset)
                args += " -%02d:%02d" % t

        sunwait = SUNWAIT_COMMAND.format(args=args)


    return DEFAULT_CRON_LINE.format(minute=minute, \
                                    hour=hour, \
                                    sunwait=sunwait, \
                                    random=random, \
                                    command=command)



def strip_comments(line):
    if COMMENT_CHAR in line:
        # remove all characters after the first comment char
        line = line[:line.index(COMMENT_CHAR)]

    return line



def main(sched_filename):
    entries = []

    with open(sched_filename, "r") as sched:
        rawlines = sched.readlines()

        for i, line in enumerate(rawlines):
            line = strip_comments(line) # remove comments
            line = line.strip() # strip newlines and leading/trailling spaces

            if not line:
                continue # skip empty lines

            cron_line = parse(line)

            if cron_line:
                entries.append(cron_line)
                print(cron_line)
            else:
                print("invalid entry (line {}): {}".format(i, repr(rawlines[i])), file=sys.stderr)





if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sched_to_crontab.py <sched_file>")
        exit()

    if os.path.isfile(sys.argv[1]):
        main(sys.argv[1])
    else:
        print("sched file doesn't exist")
        exit()
