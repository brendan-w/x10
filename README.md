X10
===

Personal X10 home automation framework based on `cron`, `br`, and `sunwait`


Porcelain Commands
------------------

- `edit_sched.sh` editor and loader for the X10 schedule file
- `x10.sh` main control script for sending x10 commands


User Files
----------

These files must be generated before the system will work. They are ignored by git.

- `location.sh`: file providing `$X10_LAT` and `$X10_LNG`
- `schedule.x10`: your schedule file, following the format in `sample.x10`
