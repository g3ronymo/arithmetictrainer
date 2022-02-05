"""
Commandline interface.
"""
import sys
import time
import os
import argparse
from pathlib import Path
from decimal import Decimal, InvalidOperation

sys.path.insert(0, str(Path(__file__).parent))
from core import Arithmetictrainer
from utils import create_taskgenerators_from_file
from __init__ import version

def parse_args():
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
            '-c',
            '--config',
            type=str,
            help='Path to configuration file'
    )
    parser.add_argument(
            '--version', action='version', version=f'%(prog)s {version}'
    )
    parser.add_argument('-w', '--web', action='store_true')
    return parser.parse_args()

def get_config(args) -> Path:
    if args.config and Path(args.config).is_file():
        config = Path(args.config)
    elif Path(os.environ.get('XDG_CONFIG_HOME', '~/.config')
        ).joinpath('arithmetictrainer/config').is_file():
        config = Path(
                os.environ.get('XDG_CONFIG_HOME', '~/.config')
                ).joinpath('arithmetictrainer/config')
    elif Path.cwd().joinpath('config').is_file():
        config = Path.cwd().joinpath('config')
    else:
        config = Path(__file__).parent.joinpath('data/config'),
    return config

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
    args = parse_args()
    if args.web:
        import webgui
        webgui.main()
    taskgen_list = create_taskgenerators_from_file(get_config(args))
    trainer = Arithmetictrainer(taskgen_list)
    started_at = time.time()
    for i in range(args.number):
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
