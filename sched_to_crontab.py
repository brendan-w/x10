#!/bin/env python3

import os
import sys
from enum import Enum

TOKEN_TYPE = Enum("time", "offset", "random")
COMMENT_CHAR = "#"
TIME_COMMAND_SEP = ";"
DEFAULT_CRON_LINE = "{minute} {hour} * * * {sunwait} ; {random} ; br {command}"


# token classifiers
time_re = re.compile(r"(\d+:\d+(am|pm))|dawn|dusk$")
offset_re = re.compile(r"[+\-]\d+$")
random_re = re.compile(r"~\d+$")



# returns iterable of letters from start to stop
# alphabet_region("a", "z") = ["a", "b", "c", ... "z"]
alphabet_region = lambda start, stop: map(chr, range(ord(start), ord(stop) + 1))


def read_time(token):
    pass


def read_offset(token):
    if "+" in token:
        offset = token[token.index("+") + 1:]
        if offset.startswith("random("):
    elif "-" in token:
        pass
    else:
        return None


def classify_token(token):
    if (token[0] in "+-") and (token[1:].isnumeric():
        return TOKEN_TYPE.offset

    if (token[0] == "~") and (token[1:].isnumeric():
        return TOKEN_TYPE.random

        return TOKEN_TYPE.time

    if 

    return None




def parse(line):
    """ Main parsing function """

    parts = line.split(TIME_COMMAND_SEP)

    if len(parts) != 2:
        return None

    time_part = parts[0].strip()
    command_part = parts[1].strip()

    # parse the time

    time_part = time_part.lower() # be case insensitive
    time_tokens = time_part.split() # tokenize by spaces

    # parse each token
    for token in time_tokens:
        
        if time_re.match(token):
            # timestamp
            pass

        elif offset_re.match(token):
            # offset
            pass

        elif random_re.match(token):
            # random
            pass

        else:
            return None # encountered unknown token, halt

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
