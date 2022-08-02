import os
from unittest import mock
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


@mock.patch('os.path.isdir')
def test_filter_results_exclude_is_dir(mock_isdir):
    mock_isdir.return_value = True
    args = {"--exclude": ["./notebook"]}
    results = ["./notebook/1.pynb", "./notebook2/1.pynb"]
    filtered = treon.filter_results(results=results, args=args)
    expected = ["./notebook2/1.pynb"]
    assert filtered == expected


@mock.patch('os.path.isdir')
def test_filter_results_exclude_is_not_dir(mock_isdir):
    mock_isdir.return_value = False
    args = {"--exclude": ["./notebook"]}
    results = ["./notebook1/1.pynb", "./notebook2/1.pynb"]
    filtered = treon.filter_results(results=results, args=args)
    expected = []
    assert filtered == expected


def test_get_notebooks_to_test_with_multiple_paths():
    args = {
        "PATH": [
            'tests/resources/basic.ipynb',
            'tests/resources/unittest_failed.ipynb',
        ],
        "--exclude": [],
    }
    notebooks = treon.get_notebooks_to_test(args=args)
    expected = [
        'tests/resources/basic.ipynb',
        'tests/resources/unittest_failed.ipynb',
    ]
    assert notebooks == expected
