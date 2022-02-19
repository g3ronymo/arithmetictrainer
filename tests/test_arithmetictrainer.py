import unittest
from decimal import Decimal
import context
from arithmetictrainer import core


class TaskgeneratorTest(unittest.TestCase):
    def setUp(self):
        self.taskgen_addition = core.Taskgenerator(core.Addition, -100, 100, 2, 1)

    def test_get_number(self):
        for i in range(100):
            num = self.taskgen_addition._get_number()
            self.assertNotEqual(num, Decimal('0'))
            self.assertTrue(num >= Decimal(-100))
            self.assertTrue(num <= Decimal(100))

class ArithmetictrainerTest(unittest.TestCase):
    def setUp(self):
        taskgens = [
                core.Taskgenerator(core.Addition, -100, 100, 2, 1),
                core.Taskgenerator(core.Subtraction, -100, 100, 2, 1),
                core.Taskgenerator(core.Multiplication, -100, 100, 2, 1),
                core.Taskgenerator(core.Division, -100, 100, 2, 1),
        ]
        self.trainer = core.Arithmetictrainer(taskgens)
        division_taskgen = core.Taskgenerator(core.Division, -100, 100, 2, 1)
        self.division_trainer = core.Arithmetictrainer([division_taskgen])

    def test_answer(self):
        current_task = self.trainer.current_task
        correct_aw = current_task['correct_answer']
        wrong_aw = correct_aw + Decimal('1')

        self.assertFalse(self.trainer.answer(wrong_aw))
        self.assertEqual(current_task, self.trainer.current_task)
        self.assertTrue(self.trainer.answer(correct_aw))
        self.assertNotEqual(current_task, self.trainer.current_task)

        self.division_trainer.answer(Decimal('0'))

if __name__ == '__main__':
    unittest.main()
