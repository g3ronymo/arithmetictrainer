"""
Commandline interface.
"""
import time
import argparse
from pathlib import Path
from decimal import Decimal, InvalidOperation

from arithmetictrainer.core import create_arithmetictrainer_from_files
from arithmetictrainer import version

from xdg import BaseDirectory

def __parse_args():
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser(
        prog="Arithmetictrainer",
        description="Train mental arithmetic",
    )
    parser.add_argument(
            '-n',
            '--number',
            type=int,
            default=10,
            help='Number of tasks to solve'
    )
    parser.add_argument(
            '-c', '--config', type=str, help='Path to configuration file'
    )
    parser.add_argument(
            '--version', action='version', version=f'%(prog)s {version}'
    )
    return parser.parse_args()

def __get_config(args) -> Path:
    config = None
    if args.config and Path(args.config).is_file():
        config = Path(args.config)
    elif BaseDirectory.load_first_config('arithmetictrainer', 'config'):
        config = BaseDirectory.load_first_config('arithmetictrainer', 'config')
    elif Path.cwd().joinpath('config').is_file():
        config = Path.cwd().joinpath('config')
    return config

def __get_answer(current_task: str, result_decimal_points: int) -> Decimal:
    """
    Get an answer for *task*. Raises KeyboardInterrupt if user input is one
    of ('q', 'quit', (exit')
    """
    print('Round to ' + str(result_decimal_points) + ' decimal points')
    numeric_answer = False
    while not numeric_answer:
        answer = input(current_task + ' = ').strip()
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
    args = __parse_args()
    config = __get_config(args)
    trainer = create_arithmetictrainer_from_files(config)
    while trainer.getNumCorrectAnswers() < args.number:
        try:
            answer = __get_answer(
                    trainer.getCurrentTask(),
                    trainer.getResultDecimalPoints(),
            )
            was_correct = trainer.answer(answer)
            if was_correct:
                print('*' * 3)
        except KeyboardInterrupt:
            break
    print()
    print('*' * 10)
    print('Solved', trainer.getNumCorrectAnswers(), 'tasks')
    print(
            'in',
            str(time.time() - trainer.getStartedAt()),
            'seconds.'
    )
    print('With', trainer.getNumIncorrectAnswers(), 'incorrect answers')
    print('*' * 10)

if __name__ == '__main__':
    main()
