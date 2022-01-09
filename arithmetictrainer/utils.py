import configparser
import arithmetictrainer
import time


def create_taskgenerators_from_file(path) -> list[arithmetictrainer.Taskgenerator]:
    """
    Great list with Objects from type Taskgenerator.
    path can be a string, path object or iterable thereof.

    The config file should be in the style of *Microsoft Windows INI* files.
    Each Section describes a taskgenerator. Each Section has to contain the
    keys shown in the example below::
        
        [SectionName]
        operator=
        variable_min=
        variable_max=
        variable_num=
        variable_decimal_points=
    """
    config = configparser.ConfigParser()
    config.read(path)
    if len(config.sections()) == 0:
        raise ValueError("Could not find a valid config in: " + str(path))
    taskgenerators = list()
    for section in config.sections():
        # get operator
         operator = config[section]['operator']
         if operator in ('+'):
             operator = arithmetictrainer.Addition
         elif operator in ('-'):
             operator = arithmetictrainer.Subtraction
         elif operator in ('*'):
             operator = arithmetictrainer.Multiplication
         elif operator in ('/'):
             operator = arithmetictrainer.Division
         else:
             raise KeyError(f'"{operator}" is not a valid operator')
         # get variable_min
         variable_min = config.getint(section, 'variable_min')
         # get variable_max
         variable_max = config.getint(section, 'variable_max')
         # get variable_num
         variable_num = config.getint(section, 'variable_num')
         # get variable_num
         variable_decimal_points = config.getint(
                 section, 'variable_decimal_points'
         )
         taskgenerators.append(arithmetictrainer.Taskgenerator(
                 operator,
                 variable_min,
                 variable_max,
                 variable_num,
                 variable_decimal_points
         ))
    return taskgenerators

