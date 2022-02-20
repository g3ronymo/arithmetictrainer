"""
Core objects.
"""
import time
import random
import functools
import decimal
from decimal import Decimal, getcontext
from abc import ABC, abstractmethod



class Operator(ABC):

    @classmethod
    @abstractmethod
    def apply(cls, variables: list[Decimal]) -> Decimal:
        """
        Apply this operator to *variables* and return the result.
        """
        pass

    @classmethod
    @abstractmethod
    def get_sign(cls) -> str:
        """
        Return the sign for this operator.
        """
        pass


class Addition(Operator):

    @classmethod
    def apply(cls, variables: list[Decimal]) -> Decimal:
        """
        Apply this operator to *variables* and return the result.
        """
        return sum(variables)

    @classmethod
    def get_sign(cls) -> str:
        """
        Return the sign for this operator.
        """
        return "+"


class Subtraction(Operator):

    @classmethod
    def apply(cls, variables: list[Decimal]) -> Decimal:
        """
        Apply this operator to *variables* and return the result.
        """
        return functools.reduce(lambda x, y: x - y, variables)

    @classmethod
    def get_sign(cls) -> str:
        """
        Return the sign for this operator.
        """
        return "-"


class Multiplication(Operator):

    @classmethod
    def apply(cls, variables: list[Decimal]) -> Decimal:
        """
        Apply this operator to *variables* and return the result.
        """
        return functools.reduce(lambda x, y: x * y, variables)

    @classmethod
    def get_sign(cls) -> str:
        """
        Return the sign for this operator.
        """
        return "*"


class Division(Operator):

    @classmethod
    def apply(cls, variables: list[Decimal]) -> Decimal:
        """
        Apply this operator to *variables* and return the result.
        """
        return functools.reduce(lambda x, y: x / y, variables)

    @classmethod
    def get_sign(cls) -> str:
        """
        Return the sign for this operator.
        """
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
        if variable_min >= variable_max:
            raise ValueError('"variable_min" is not less than "variable_max"')
        if variable_num < 2:
            raise ValueError('"variable_num" can not be less than 2')
        if variable_decimal_points < 0:
            raise ValueError('"variable_decimal_points" can not be less than zero')
        self.variable_min = variable_min
        self.variable_max = variable_max
        self.operator = operator
        self.variable_num = variable_num
        self.variable_decimal_points = variable_decimal_points

    def get_task(self) -> dict:
        """
        Return a dictonary which describe's a task.::

            {
                'task': str,
                'result_decimal_points': int,
                'correct_answer': Decimal,
            }
        """
        task = dict()
        variables = self._get_number_array(self.variable_num)
        x = self.operator.apply(variables)
        task['correct_answer'] = round(x, self.variable_decimal_points)
        task['result_decimal_points'] = self.variable_decimal_points
        task_str = ""
        for i in range(len(variables)-1):
            task_str += str(variables[i]) + ' ' + self.operator.get_sign()
        task_str += ' ' + str(variables[-1])
        task['task'] = task_str
        return task

    def _get_number(self, allow_zero=False) -> Decimal:
        """
        Get a Decimal in range [min, max].
        The number is rounded to  self.variable_decimal__points.
        """
        getcontext().rounding = decimal.ROUND_HALF_UP
        x = random.randint(
                self.variable_min, self.variable_max) * random.random()
        x = Decimal(x)
        x = round(x, self.variable_decimal_points)
        while x == Decimal('0') and not allow_zero:
            x = random.randint(
                    self.variable_min, self.variable_max) * random.random()
            x = Decimal(x)
            x = round(x, self.variable_decimal_points)
        return x

    def _get_number_array(self, num_vars, allow_zero=False) -> list[Decimal]:
        """Get a list with generated Decimal numbers"""
        l = []
        for i in range(num_vars):
            l.append(self._get_number(allow_zero=allow_zero))
        return l

class BaseArithmetictrainer:

    def __init__(self, taskgenerators: list):
        self.taskgenerators = taskgenerators
        self.__next__()

    def __next__(self):
        self.current_task = random.choice(self.taskgenerators).get_task()


class Arithmetictrainer(BaseArithmetictrainer):
    """
    .. code:: Python

        trainer = Arithmetictrainer(taskgens)
        trainer.start()
        while trainer.solvedTasks() < 10:
            trainer.getTask()
            trainer.answer()
        stats = trainer.getStats()
        
    """
    
    def __init__(self, taskgenerators: list):
        self.num_incorrect_answers = 0
        self.num_correct_answers = 0
        super().__init__(taskgenerators)

    def start(self):
        """
        Start/Reset Arithmetictrainer.
        """
        self.num_incorrect_answers = 0
        self.num_correct_answers = 0
        self.time_started = time.time()
        self.__next__()

    def solvedTasks(self) -> int:
        """
        Return the number of solved tasks.
        """
        return self.num_correct_answers

    def getTask(self) -> dict:
        """Get the current task"""
        return self.current_task

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

    def getStats(self) -> dict:
        """
        Get statistics to the solved tasks.
        Valid keyes are:

        - time_since_start
        - num_correct_answers
        - num_correct_answers

        """
        stats = {
                    'time_since_start': time.time() - self.time_started,
                    'num_incorrect_answers': self.num_incorrect_answers,
                    'num_correct_answers': self.num_correct_answers,
                 }
        return stats


