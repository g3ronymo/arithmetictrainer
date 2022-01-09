"""
Commandline interface.
"""
import sys
import time
import argparse
from decimal import Decimal, InvalidOperation
from arithmetictrainer import Arithmetictrainer
from utils import create_taskgenerators_from_file

def get_answer(task: dict) -> Decimal:
    """
    Get an answer for *task*. Raises KeyboardInterrupt if user input is one
    of ('q', 'quit', (exit')
    """
    print('Round to ' + str(task['result_decimal_points']) + ' decimal points')
    numeric_answer = False
    while not numeric_answer:
        answer = input(task['task'] + ' = ').strip()
        if answer in ('q', 'quit', 'exit'):
            raise KeyboardInterrupt
        try:
            answer = Decimal(answer)
            numeric_answer = True
        except InvalidOperation:
            answer = False
            numeric_answer = False
    return answer


def main():
    parser = argparse.ArgumentParser(
        prog="Arithmetictrainer",
        description="Train mental arithmetic",
    )
    parser.add_argument(
            '-n',
            '--number-of-tasks',
            type=int,
            default=10,
            help='Number of tasks to solve'
    )
    args = parser.parse_args()
    possible_config_places = [
        'config',
        'data/config',
    ]
    taskgen_list = create_taskgenerators_from_file(possible_config_places)
    trainer = Arithmetictrainer(taskgen_list)
    started_at = time.time()
    for i in range(args.number_of_tasks):
        answer = False
        while not answer:
            try:
                answer = get_answer(trainer.getTask())
            except KeyboardInterrupt:
                sys.exit()
            answer = trainer.answer(answer)
        print('-' * 3)
    seconds_needed = time.time() - started_at
    print('*' * 10)
    print(f'Solved {trainer.num_correct_answers} tasks')
    print(f'in {seconds_needed} seconds.')
    print(f'With {trainer.num_incorrect_answers} incorrect answers')
    print('*' * 10)


if __name__ == '__main__':
    main()
