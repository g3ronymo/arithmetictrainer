import time
import random
import functools
import decimal
import json
import configparser
from decimal import Decimal, getcontext, InvalidOperation


def _get_number(
    var_min, var_max, decimal_points, allow_zero=False) -> Decimal:
    """
    Get a random Decimal number in range [var_min, var_max].
    The number is rounded to  variable_decimal_points.
    """
    if var_min >= var_max:
        raise ValueError('"var_min" >= "var_max"')
    if decimal_points < 0:
        raise ValueError('"decimal_points" < 0')
    getcontext().rounding = decimal.ROUND_HALF_UP
    x = random.randint(var_min, var_max) * random.random()
    x = Decimal(x)
    x = round(x, decimal_points)
    while x == Decimal('0') and not allow_zero:
        x = random.randint(var_min, var_max) * random.random()
        x = Decimal(x)
        x = round(x, decimal_points)
    return x


def _get_number_array(num_vars, var_min, var_max, decimal_points,
    allow_zero=False) -> list[Decimal]:
    """
    Get a list with random Decimal numbers. 
    The numbers are in range [var_min, var_max] and rounded to 
    variable_decimal_points.
    """
    l = []
    for i in range(num_vars):
        l.append(_get_number(
            var_min, var_max, decimal_points, allow_zero=allow_zero))
    return l


class Arithmetictrainer:

    def __init__(self, config: list[dict]):
        """
        *config* each dictonary in the list has to contain the following keyes:

            operator: str
                A sign which describes the operator.
            variable_num: int
                The number of variables
            variable_min: int
                The smallest possible variable
            variable_max: int
                The largest possible variable
            variable_decimal_points: int
                The decimal points of each variable
            result_decimal_points: int
                The decimal points the result is rounded to.
        """
        if len(config) <= 0:
            raise ValueError('Not a valid config')
        self.config = config
        self.reset()
        
            

    def reset(self):
        """Reset this Arithmetictrainer"""
        self.started_at = time.time()
        self.num_correct_answers = 0
        self.num_incorrect_answers = 0
        # set by __next__
        self.current_task = None
        self.correct_answer = None
        self.result_decimal_points = None
        next(self)

    def getStartedAt(self) -> float:
        """
        Return the time this Aritmetictrainer was created or the last time the
        reset function was called as a Unix timestamp
        (Seconds since the Epoch).
        """
        return self.started_at

    def getNumCorrectAnswers(self) -> int:
        """Returns the number of correct Answers"""
        return self.num_correct_answers

    def getNumIncorrectAnswers(self) -> int:
        """Returns the number of incorrect Answers"""
        return self.num_incorrect_answers

    def getCurrentTask(self) -> str:
        """Return the current task as string"""
        return self.current_task

    def getCorrectAnswer(self) -> Decimal:
        """Return the correct answer for the current task"""
        return self.correct_answer

    def getResultDecimalPoints(self) -> int:
        """
        Return the number of decimal points the result of the
        current task is rounded to
        """
        return self.result_decimal_points

    def getConfig(self) -> list[dict]:
        """Get the config of Arithmetictrainer."""
        return self.config

    def answer(self, answer: str | Decimal):
        """
        Answer the current_task. If answer was correct return true, else false
        """
        try:
            answer = Decimal(answer)
        except InvalidOperation:
            answer = None
        if answer == self.getCorrectAnswer():
            self.num_correct_answers += 1
            next(self)
            return True
        self.num_incorrect_answers += 1
        return False

    
    def __next__(self):
        """
        Set and Return the next task
        """
        conf = random.choice(self.config)
        variables = _get_number_array(
                conf['variable_num'], 
                conf['variable_min'],
                conf['variable_max'],
                conf['variable_decimal_points'],
        )
        match conf['operator']:
            case '+':
                correct_answer = sum(variables)
            case '-':
                correct_answer = functools.reduce(lambda x, y: x - y, variables)
            case '*':
                correct_answer = functools.reduce(lambda x, y: x * y, variables)
            case '/' | ':':
                correct_answer = functools.reduce(lambda x, y: x / y, variables)
            case _:
                raise ValueError(
                    str(conf["operator"]) + ' is not a valid operator')
        self.correct_answer = round(
                correct_answer, conf['variable_decimal_points'])
        self.current_task = functools.reduce(
                lambda x, y: '{} {} {}'.format(x, conf['operator'], y), variables)
        self.result_decimal_points = conf['variable_decimal_points']

def create_arithmetictrainer_from_files(*files) -> Arithmetictrainer:
    """
    Create a Arithmetictrainer from a configuration file.
    """
    config_files = configparser.ConfigParser()
    config_files.read(*files)
    if len(config_files.sections()) == 0:
        raise ValueError("Could not find a valid config in: ", *files)
    config = []
    for section in config_files.sections():
        tmp = {}
        tmp['operator'] = config_files[section]['operator']
        tmp['variable_num'] = config_files.getint(section, 'variable_num')
        tmp['variable_min'] = config_files.getint(section, 'variable_min')
        tmp['variable_max'] = config_files.getint(section, 'variable_max')
        tmp['variable_decimal_points'] = config_files.getint(
                section, 'variable_decimal_points')
        tmp['result_decimal_points'] = config_files.getint(
                section, 'result_decimal_points')
        config.append(tmp)
    return Arithmetictrainer(config)

