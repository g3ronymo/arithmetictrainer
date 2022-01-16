import random
import functools
import decimal
from decimal import Decimal, getcontext
from abc import ABC, abstractmethod


class NumberGenerator:
    """Generat numbers"""

    def __init__(self, min_value: int, max_value: int, decimal_points: int):
        self.min_value = min_value
        self.max_value = max_value
        self.decimal_points = decimal_points

    def get_number(self, allow_zero=False) -> Decimal:
        """
        Get a number in range [min, max].
        The number is rounded to  decimal_points.
        """
        getcontext().rounding = decimal.ROUND_HALF_UP
        x = random.randint(self.min_value, self.max_value) * random.random()
        x = Decimal(x)
        x = round(x, self.decimal_points)
        while not allow_zero and x == Decimal(0):
            x = random.randint(self.min_value, self.max_value) * random.random()
            x = Decimal(x)
            x = round(x, self.decimal_points)
        return x

    def get_number_array(self, n: int, allow_zero=False) -> list[Decimal]:
        """Get a list with generated numbers"""
        l = []
        for i in range(n):
            l.append(self.get_number(allow_zero=allow_zero))
        return l


class Operator(ABC):

    @classmethod
    @abstractmethod
    def apply(cls, variables: list[Decimal]) -> Decimal:
        pass

    @classmethod
    @abstractmethod
    def get_sign(cls) -> str:
        pass


class Addition(Operator):

    @classmethod
    def apply(cls, variables: list[Decimal]) -> Decimal:
        return sum(variables)

    @classmethod
    def get_sign(cls) -> str:
        return "+"


class Subtraction(Operator):

    @classmethod
    def apply(cls, variables: list[Decimal]) -> Decimal:
        return functools.reduce(lambda x, y: x - y, variables)

    @classmethod
    def get_sign(cls) -> str:
        return "-"


class Multiplication(Operator):

    @classmethod
    def apply(cls, variables: list[Decimal]) -> Decimal:
        return functools.reduce(lambda x, y: x * y, variables)

    @classmethod
    def get_sign(cls) -> str:
        return "*"


class Division(Operator):

    @classmethod
    def apply(cls, variables: list[Decimal]) -> Decimal:
        return functools.reduce(lambda x, y: x / y, variables)

    @classmethod
    def get_sign(cls) -> str:
        return "/"


class Taskgenerator:
    """Generat Tasks"""

    def __init__(
            self,
            operator: Operator,
            variable_min: int,
            variable_max: int,
            variable_num: int,
            variable_decimal_points: int
            ):
        self.operator = operator
        self.variable_num = variable_num
        self.variable_decimal_points = variable_decimal_points
        self.number_generator = NumberGenerator(
                variable_min, variable_max, variable_decimal_points
        )

    def get_task(self) -> dict:
        """
        Return a dictonary which describe's a task.::

            {
                'task':str,
                'result_decimal_points':int,
                'correct_answer':Decimal,
            }
        """
        task = dict()
        variables = self.number_generator.get_number_array(self.variable_num)
        x = self.operator.apply(variables)
        task['correct_answer'] = round(x, self.variable_decimal_points)
        task['result_decimal_points'] = self.variable_decimal_points
        task_str = ""
        for i in range(len(variables)-1):
            task_str += str(variables[i]) + ' ' + self.operator.get_sign()
        task_str += ' ' + str(variables[-1])
        task['task'] = task_str
        return task


class Arithmetictrainer:

    def __init__(self, taskgenerators: list):
        self.taskgenerators = taskgenerators
        self.num_incorrect_answers = 0
        self.num_correct_answers = 0
        self.__next__()

    def __next__(self):
        self.current_task = random.choice(self.taskgenerators).get_task()

    def answer(self, answer: Decimal) -> bool:
        """
        Answer the current task. If the answer is correct return True,
        else False.
        """
        if answer.compare(self.current_task['correct_answer']) == Decimal('0'):
            self.num_correct_answers += 1
            self.__next__()
            return True
        self.num_incorrect_answers += 1
        return False

    def getTask(self) -> dict:
        """Get the current task"""
        return self.current_task
