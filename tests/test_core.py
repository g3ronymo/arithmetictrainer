import unittest
import time
import json
from decimal import Decimal

from arithmetictrainer.core import Arithmetictrainer


class ArithmetictrainerTest(unittest.TestCase):
    def setUp(self):
        config = [{
                'operator': '+',
                'variable_num': 2,
                'variable_min': -100,
                'variable_max': 100,
                'variable_decimal_points': 1,
                'result_decimal_points': 1,
        }]
        self.trainer = Arithmetictrainer(config)

    def test__init__(self):
        config = [{
                'operator': '+',
                'variable_num': 2,
                'variable_min': -100,
                'variable_max': 100,
                'variable_decimal_points': 1,
                'result_decimal_points': 1,
        }]
        a = Arithmetictrainer(config)
        self.assertTrue(a.getConfig() == config)

    def test_answer(self):
        correct_answer = self.trainer.getCorrectAnswer()
        wrong_answer = str(Decimal(correct_answer) + 1)

        self.assertEqual(0, self.trainer.getNumCorrectAnswers())
        self.assertFalse(self.trainer.answer(wrong_answer))
        self.assertEqual(0, self.trainer.getNumCorrectAnswers())
        self.assertTrue(self.trainer.answer(correct_answer))
        self.assertEqual(1, self.trainer.getNumCorrectAnswers())

if __name__ == '__main__':
    unittest.main()
