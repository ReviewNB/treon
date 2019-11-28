import os
from treon import treon

def test_filter_results_file():
    args = {
        "--exclude": ['resources/basic.ipynb',
                      'failed']
    }
    results = ['resources/basic.ipynb',
               'resources/doctest_failed.ipynb',
               'resources/runtime_error.ipynb',
               'resources/unittest_failed.ipynb',
               'other/resources.ipynb']

    filtered = treon.filter_results(results=results, args=args)
    expected = ['resources/doctest_failed.ipynb',
                'resources/runtime_error.ipynb',
                'resources/unittest_failed.ipynb',
                'other/resources.ipynb']
    assert filtered == expected


def test_filter_results_folder():
    args = {"--exclude": ['resources']}
    results = ['resources/basic.ipynb',
               'resources/doctest_failed.ipynb',
               'resources/runtime_error.ipynb',
               'resources/unittest_failed.ipynb',
               'other/resources.ipynb']

    filtered = treon.filter_results(results=results, args=args)
    expected = ['other/resources.ipynb']
    assert filtered == expected


def test_filter_results_empty():
    args = {"--exclude": ['resources']}
    results = ['resources/basic.ipynb']
    filtered = treon.filter_results(results=results, args=args)
    expected = []
    assert filtered == expected


def test_filter_results_homedir():
    args = {"--exclude": ['~/resources']}
    results = [os.path.join(os.path.expanduser("~"), "resources/basic.ipynb")]
    filtered = treon.filter_results(results=results, args=args)
    expected = []
    assert filtered == expected
