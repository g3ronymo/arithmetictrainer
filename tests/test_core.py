import unittest
import time
import json
from decimal import Decimal

import context

from arithmetictrainer.core import get_number
from arithmetictrainer.core import get_number_array
from arithmetictrainer.core import Arithmetictrainer
from arithmetictrainer.core import arithmetictrainerFromJson


class GetNumberTest(unittest.TestCase):

    def test_get_number(self):
        self.assertRaises(ValueError, get_number, 2, 2, 1)
        self.assertRaises(ValueError, get_number, 2, 4, -1)
        for i in range(100):
            num = get_number(-100, 100, 1)
            self.assertNotEqual(num, Decimal('0'))
            self.assertTrue(num >= Decimal(-100))
            self.assertTrue(num <= Decimal(100))

    def test_get_number_array(self):
        num = get_number_array(0, -100, 100, 1)
        self.assertEqual(len(num), 0)
        num = get_number_array(1, -100, 100, 1)
        self.assertEqual(len(num), 1)


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
        state = {
                'started_at': time.time(),
                'num_correct_answers': 0,
                'num_incorrect_answers': 0,
        }
        self.trainer = Arithmetictrainer(config, state=state)

    def test__init__(self):
        config = [{
                'operator': '+',
                'variable_num': 2,
                'variable_min': -100,
                'variable_max': 100,
                'variable_decimal_points': 1,
                'result_decimal_points': 1,
        }]
        state = {
                'started_at': time.time(),
                'num_correct_answers': 0,
                'num_incorrect_answers': 0,
        }
        a = Arithmetictrainer(config, state=state)
        self.assertTrue(a.getConfig() == config)
        self.assertTrue(a.getState() == state)

    def test_answer(self):
        task = self.trainer.getTask()
        correct_answer = task['correct_answer']
        wrong_answer = str(Decimal(correct_answer) + 1)

        self.assertEqual(0, self.trainer.getState()['num_correct_answers'])
        self.assertFalse(self.trainer.answer(wrong_answer))
        self.assertEqual(0, self.trainer.getState()['num_correct_answers'])
        self.assertTrue(self.trainer.answer(correct_answer))
        self.assertEqual(1, self.trainer.getState()['num_correct_answers'])


class ArithmetictrainerJsonTest(unittest.TestCase):

    def setUp(self):
        config = [{
                'operator': '+',
                'variable_num': 2,
                'variable_min': -100,
                'variable_max': 100,
                'variable_decimal_points': 1,
                'result_decimal_points': 1,
        }]
        state = {
                'started_at': time.time(),
                'num_correct_answers': 0,
                'num_incorrect_answers': 0,
        }
        self.trainer = Arithmetictrainer(config, state=state)


    def test_decode_encode(self):
        j = json.dumps(self.trainer.toJsonSerializable())
        decoded_trainer = arithmetictrainerFromJson(j)
        self.assertTrue(self.trainer == decoded_trainer)

if __name__ == '__main__':
    unittest.main()
