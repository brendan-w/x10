
# All entries follow this format. Whitespace matters.
#
#    <TIME> <OFFSET> <RANDOMNESS> ; <X10_CODE> <X10_COMMAND>
#
#
# The <TIME> <OFFSET> <RANDOMNESS> parts can be in any order, as long as they
# come before the semicolon.


# <TIME> can be:
#    1:13pm       A hard coded time
#    01:13PM      Different case and leading zeros are fine
#    dusk         An astronomical event (dusk or dawn)
#    dawn

# <OFFSET> is optional, and can be:
#    +5           minutes AFTER the specified time
#    -5           minutes BEFORE the specified time

# <RANDOMNESS> is optional, can be:
#    ~5           will pick a random positive offset between 0 and X minutes
#                 this random offset will be ADDED to any previous specified offsets
#                 NOTE: ~X can only be used as a positive offset (AFTER the time)

# <X10_CODE> <X10_COMMAND> can be:
#    C2 ON
#    C2 OFF


# Here are some sample entries:

2:00am ; C1 OFF            # turns off C1 at 2:00am
2:00am -30 ; C1 OFF        # turns off C1 at 1:30am
2:00am -30 ~15 ; C1 OFF    # turns off C1 at a random time between 1:30am and 1:45am
dusk ; C1 ON               # turns on C1 at dusk
dusk +15 ; C1 ON           # turns on C1 15 minutes AFTER dusk
dusk -15 ; C1 ON           # turns on C1 15 minutes BEFORE dusk
dusk ~15 ; C1 ON           # turns on C1 at a random time between dusk, and 15 minutes AFTER dusk
dusk +30 ~15 ; C1 ON       # turns on C1 at a random time between "30 minutes after dusk" and "45 minutes after dusk"
