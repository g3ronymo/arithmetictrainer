import unittest
from decimal import Decimal
import context
from arithmetictrainer import arithmetictrainer as ar

class NumberGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.numgen = ar.NumberGenerator(-100, 100, 1)

    def test_get_number(self):
        for i in range(100):
            num = self.numgen.get_number()
            self.assertNotEqual(num, Decimal('0'))
            self.assertTrue(num >= Decimal(-100))
            self.assertTrue(num <= Decimal(100))

class ArithmetictrainerTest(unittest.TestCase):
    def setUp(self):
        taskgens = [
                ar.Taskgenerator(ar.Addition, -100, 100, 2, 1),
                ar.Taskgenerator(ar.Subtraction, -100, 100, 2, 1),
                ar.Taskgenerator(ar.Multiplication, -100, 100, 2, 1),
                ar.Taskgenerator(ar.Division, -100, 100, 2, 1),
        ]
        self.trainer = ar.Arithmetictrainer(taskgens)

    def test_answer(self):
        current_task = self.trainer.current_task
        correct_aw = current_task['correct_answer']
        wrong_aw = correct_aw + Decimal('1')

        self.assertFalse(self.trainer.answer(wrong_aw))
        self.assertEqual(current_task, self.trainer.current_task)
        self.assertTrue(self.trainer.answer(correct_aw))
        self.assertNotEqual(current_task, self.trainer.current_task)

if __name__ == '__main__':
    unittest.main()
