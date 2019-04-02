"""
Usage:
  treon
  treon PATH

Arguments:
  PATH          File or directory path to find notebooks to test. Searches recursively for directory paths. Default: current working directory.

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

__version__ = "0.1.0"


import sys
import os
import glob
from docopt import docopt, DocoptExit
from multiprocessing import Pool as ProcessPool

from .task import Task

PROCESS_COUNT = 10


def main():
    try:
        arguments = docopt(__doc__, version=__version__)
        print(arguments)
    except DocoptExit:
        sys.exit(__doc__)

    print('Executing treon version %s' % __version__)
    notebooks = get_notebooks_to_test(arguments)
    tasks = [Task(notebook) for notebook in notebooks]
    print_test_collection(notebooks)
    trigger_tasks(tasks)
    print_test_result(tasks)


def trigger_tasks(tasks):
    pool = ProcessPool(PROCESS_COUNT)
    pool.map(Task.run_tests, tasks)


def print_test_result(tasks):
    succeeded = [t.file_path for t in tasks if t.is_successful]
    failed = [t.file_path for t in tasks if not t.is_successful]
    variables = {
        'succeeded_count': len(succeeded),
        'failed_count': len(failed),
        'total': len(tasks)
    }

    message = """
       -----------------------------------------------------------------------
       TEST RESULT
       -----------------------------------------------------------------------\n
    """
    message += '       -- PASSED \n'.join(succeeded) + '\n'
    message += '       -- FAILED \n'.join(failed) + '\n'
    message += '-----------------------------------------------------------------------\n'
    message += '{succeeded_count} succeeded, {failed_count} failed, out of {total} notebooks tested.'.format(**variables)
    print(message)


def print_test_collection(notebooks):
    message = """
       -----------------------------------------------------------------------
       Collected following Notebooks for testing
       -----------------------------------------------------------------------\n
    """
    message += '\n'.join(notebooks) + '\n'
    message += '-----------------------------------------------------------------------\n'
    print(message)


def get_notebooks_to_test(args):
    path = args['PATH'] or os.getcwd()
    result = []

    if os.path.isdir(path):
        print('Recursively scanning {path} for Notebooks...'.format(path=path))
        path = os.path.join(path, '')  # adds trailing slash (/) if it's missing
        glob_path = path + '**/*.ipynb'
        result = glob.glob(glob_path, recursive=True)
    elif os.path.isfile(path):
        if path.lower().endswith('.ipynb'):
            print('Testing notebook {path}'.format(path=path))
            result = [path]
        else:
            sys.exit('{path} is not a Notebook'.format(path=path))
    else:
        sys.exit('{path} is not a valid path'.format(path=path))

    if not result:
        sys.exit('No notebooks to test in {path}'.format(path=path))

    return result
