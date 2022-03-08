###############################################################################
Arithmetictrainer 
###############################################################################

``Arithmetictrainer`` can be used to practice mental arithmetic.
There are no dependencies besides python >=3.10.

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

The default configuration is::

    [Addition]
    operator=+
    variable_num=2
    variable_min=-100
    variable_max=100
    variable_decimal_points=1
    result_decimal_points=1

    [Subtraction]
    operator=-
    variable_num=2
    variable_min=-100
    variable_max=100
    variable_decimal_points=1
    result_decimal_points=1

    [Multiplication]
    operator=*
    variable_num=2
    variable_min=-100
    variable_max=100
    variable_decimal_points=0
    result_decimal_points=0

    [Division]
    operator=/
    variable_num=2
    variable_min=-100
    variable_max=100
    variable_decimal_points=0
    result_decimal_points=0


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

*******************************************************************************
Development
*******************************************************************************

Tests
=====

python -m unittest discover -v -s tests/
