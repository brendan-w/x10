#!/bin/env python3

import os
import sys
import re


COMMENT_CHAR = "#"
TIME_COMMAND_SEP = ";"
DEFAULT_CRON_LINE = "{minute} {hour} * * * {sunwait} ; {random} ; br {command}"


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

    parts = line.split(TIME_COMMAND_SEP)

    if TIME_COMMAND_SEP not in line:
        return None

    # get the position of the first seperator
    sep_pos = line.index(TIME_COMMAND_SEP)

    # split into the time and command portions
    # and strip off any leading/trailing spaces
    time_part = parts[:sep_pos].strip()
    command_part = parts[sep_pos+1:].strip()



    # parse the time

    time_part = time_part.lower() # be case insensitive
    time_tokens = time_part.split() # tokenize by spaces


    time = (0, 0) # (hour, minute) in military time
    astro = None
    offset = 0
    random = 0


    # parse each token
    for token in time_tokens:
        
        if time_re.match(token):
            # timestamp
            pass

        elif astro_re.match(token):
            astro = token
        elif offset_re.match(token):
            offset = int(token)
        elif random_re.match(token):
            random = int(token[1:])
        else:
            return None # encountered unknown token, halt

    # if this is a hard coded time
    if not astro:
        time = time_add_minutes(time, offset)


    # build the parsed data into a cron line

    cron_line = DEFAULT_CRON_LINE




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

            if not line:
                continue # skip empty lines

            cron_line = parse(tokens)

            if entry.valid():
                entries.append(entry)
            else:
                print("invalid entry (line {}): {}".format(i, rawlines[i]))

    print(entries)




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sched_to_crontab.py <sched_file>")
        exit()

    if os.path.isfile(sys.argv[1]):
        main(sys.argv[1])
    else:
        print("sched file doesn't exist")
        exit()
