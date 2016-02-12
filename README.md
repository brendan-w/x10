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
