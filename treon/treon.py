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

from .sanity import run as trigger_sanity_tests

def main():
    try:
        arguments = docopt(__doc__, version=__version__)
        print(arguments)
    except DocoptExit:
        sys.exit(__doc__)

    print('Executing treon version %s' % __version__)
    all_notebooks = get_notebooks_to_test(arguments)
    trigger_sanity_tests(all_notebooks)


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
