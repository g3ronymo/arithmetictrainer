###############################################################################
Arithmetictrainer 
###############################################################################

``Arithmetictrainer`` can be used to practice basic arithmetic.

Depends on:

- python >=3.10.
- pyxdg (https://freedesktop.org/wiki/Software/pyxdg/)

*******************************************************************************
Configuration
*******************************************************************************

If called as a commandline program a configuration file ``config`` is searched
in the following places:

1. ${XDG_CONFIG_HOME}/arithmetictrainer/config
2. ${HOME}/.config/arithmetictrainer/config
3. the current working directory

A configuration file can also be specified with::

    arithmetictrainer -c configfile

A configuration template can be found under: arithmetictrainer/data/config

Configuration options
=====================

operator
    Is one of ``+ - * /``.

variable_num
    Can be any integer but should be at least 2.

variable_min
    Can be any integer but should be smaller than *variable_max*

variable_max
    Can be any integer but should be greater than *variable_min*

variable_decimal_points
    Can be any integer but should be at least 0.

result_decimal_points
    Can be any integer but should be at least 0.
