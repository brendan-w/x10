X10
===

Personal X10 home automation framework based on `cron`, `br`, and `sunwait`


Installation
------------

These instructions are for installation on a Raspberry Pi

- create an `x10` user with home directory `/home/x10`
- add `x10` user to the `dialout` group with `usermod -a -G dialout x10`
- compile and install [`br`](http://www.linuxha.com/bottlerocket/)
- compile and install [`sunwait`](http://risacher.org/sunwait/)
- clone into the home directory with `git clone https://github.com/brendan-w/x10.git ~/`
- update your schedule with `~/edit_x10.sh`


Porcelain Commands
------------------

- `edit_sched.sh` editor and loader for the X10 schedule file
- `x10.sh` main control script for sending X10 commands
- `whenis.sh` wrapper around `sunwait` for easily reading dusk/dawn times


User Files
----------

These files must be generated before the system will work. They are ignored by git.

- `location.sh`: file providing `$X10_LAT` and `$X10_LNG`
- `schedule.x10`: your schedule file, following the format in `sample.x10`


X10 Schedule
------------

X10 Schedule files follow this format:

```shell
# <TIME>|dusk|dawn [+|-<OFFSET>] [~<RANDOMNESS>] ; <X10_CODE> <X10_COMMAND>

# for instance:

2:00am ; C1 OFF            # turns off C1 at 2:00am
2:00am -30 ; C1 OFF        # turns off C1 at 1:30am
2:00am -30 ~15 ; C1 OFF    # turns off C1 at a random time between 1:30am and 1:45am
dusk ; C1 ON               # turns on C1 at dusk
dusk +15 ; C1 ON           # turns on C1 15 minutes AFTER dusk
dusk -15 ; C1 ON           # turns on C1 15 minutes BEFORE dusk
dusk ~15 ; C1 ON           # turns on C1 at a random time between dusk, and 15 minutes AFTER dusk
dusk +30 ~15 ; C1 ON       # turns on C1 at a random time between "30 minutes after dusk", and 15 minutes AFTER "30 minutes after dusk"

```
