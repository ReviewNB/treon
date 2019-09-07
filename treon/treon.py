# pylint: disable=line-too-long
"""
Usage:
  treon
  treon [PATH] [--threads=<number>] [-v]

Arguments:
  PATH                File or directory path to find notebooks to test. Searches recursively for directory paths. [default: current working directory]

Options:
  --threads=<number>  Number of parallel threads. Each thread processes one notebook file at a time. [default: 10]
  -v --verbose        Print detailed output for debugging.
  -h --help           Show this screen.
  --version           Show version.

"""

__version__ = "0.1.2"


import glob
import logging
import pathlib
import os
import sys
import textwrap
from multiprocessing.dummy import Pool as ThreadPool
from docopt import docopt, DocoptExit

from .task import Task

DEFAULT_THREAD_COUNT = 10

LOG = logging.getLogger('treon')


def main():
    try:
        arguments = docopt(__doc__, version=__version__)
    except DocoptExit:
        sys.exit(__doc__)

    setup_logging(arguments)
    LOG.info('Executing treon version %s', __version__)
    thread_count = arguments['--threads'] or DEFAULT_THREAD_COUNT
    notebooks = get_notebooks_to_test(arguments)
    tasks = [Task(notebook) for notebook in notebooks]
    print_test_collection(notebooks)
    trigger_tasks(tasks, thread_count)
    has_failed = print_test_result(tasks)

    if has_failed:
        sys.exit(-1)


def setup_logging(arguments):
    logging.basicConfig(format='%(message)s')
    LOG.setLevel(loglevel(arguments))


def loglevel(arguments):
    verbose = arguments['--verbose']
    return logging.DEBUG if verbose else logging.INFO


def trigger_tasks(tasks, thread_count):
    pool = ThreadPool(int(thread_count))
    pool.map(Task.run_tests, tasks)


def print_test_result(tasks):
    has_failed = False
    succeeded = [t.file_path for t in tasks if t.is_successful]
    failed = [t.file_path for t in tasks if not t.is_successful]
    variables = {
        'succeeded_count': len(succeeded),
        'failed_count': len(failed),
        'total': len(tasks)
    }

    message = textwrap.dedent("""
              -----------------------------------------------------------------------
              TEST RESULT
              -----------------------------------------------------------------------\n""")

    if succeeded:
        message += '       -- PASSED \n'.join(succeeded) + '       -- PASSED \n'

    if failed:
        has_failed = True
        message += '       -- FAILED \n'.join(failed) + '       -- FAILED \n'

    message += '-----------------------------------------------------------------------\n'
    message += '{succeeded_count} succeeded, {failed_count} failed, out of {total} notebooks tested.\n'.format(**variables)
    message += '-----------------------------------------------------------------------\n'
    LOG.info(message)
    return has_failed


def print_test_collection(notebooks):
    message = textwrap.dedent("""
              -----------------------------------------------------------------------
              Collected following Notebooks for testing
              -----------------------------------------------------------------------\n""")
    message += '\n'.join(notebooks) + '\n'
    message += '-----------------------------------------------------------------------\n'
    LOG.debug(message)


def get_notebooks_to_test(args):
    path = pathlib.Path(args['PATH'] or os.getcwd())

    if path.is_file():
        if path.suffix == '.ipynb':
            return [path.as_posix()]
        sys.exit("{path} is not a notebook".format(path=path))
    elif path.is_dir():
        LOG.info("Recursively scanning %s for notebooks...", path)
        ignored = build_ignore_list(path)
        notebooks = filter(lambda nb: nb not in ignored, path.glob('**/*.ipynb'))
        notebooks = list((nb.as_posix() for nb in notebooks))
        if not notebooks:
            sys.exit("No notebooks to test in {path}".format(path=path))
        return notebooks
    else:
        sys.exit("{path} is not a valid path".format(path=path))


def build_ignore_list(search_directory):
    """
    Recursively searches a given directory for `.treonignore` files and
    compiles a list of :class:`pathlib.Path` objects that should be ignored.
    Note that this function does not return the rules specified in any
    `.treonignore` files but instead paths to the notebooks that should
    be ignored once the parsed rules are applied.

    :param pathlib.Path search_directory: directory to search
    """
    # For each .treonignore file in search_directory or its children...
    for ignorefile in search_directory.glob('**/.treonignore'):
        LOG.debug("Found ignore file %s", ignorefile.as_posix())
        # Iterate over all of the rules in the .treonignore file...
        with ignorefile.open() as rules:
            for rule in rules:
                rule = rule.strip().lstrip(os.sep)
                rule = ignorefile.parent.joinpath(rule).as_posix()
                # And find any notebooks that match those rules.
                if os.path.isdir(rule):
                    rule = os.path.join(rule, '**')
                LOG.debug("Adding ignore rule %s", rule)
                for match in glob.iglob(rule):
                    if match.endswith('.ipynb'):
                        LOG.debug("Ignore file %s matches %r",
                                  ignorefile.as_posix(), match)
                        yield match
