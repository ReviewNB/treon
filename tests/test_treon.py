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
    notebook_files = [
        os.path.join(os.path.dirname(__file__), "resources/basic.ipynb"),
        os.path.join(os.path.dirname(__file__), "resources/unittest_failed.ipynb"),
    ]
    args = {
        "PATH": list(notebook_files),
        "--exclude": [],
    }
    notebooks = treon.get_notebooks_to_test(args=args)
    expected = notebook_files
    assert notebooks == expected


def test_get_notebooks_to_test_with_multiple_dir_paths():
    cwd = os.path.dirname(__file__)
    notebook_folders = [
        os.path.join(cwd, "resources"),
        os.path.join(cwd, "resources-2")
    ]
    expected = [os.path.join(cwd, 'resources/unittest_failed.ipynb'),
                os.path.join(cwd, 'resources/runtime_error.ipynb'),
                os.path.join(cwd, 'resources/basic.ipynb'),
                os.path.join(cwd, 'resources/doctest_failed.ipynb'),
                os.path.join(cwd, 'resources-2/a1.ipynb'),
                os.path.join(cwd, 'resources-2/b1.ipynb')]
    args = {
        "PATH": list(notebook_folders),
        "--exclude": [],
    }
    notebooks = treon.get_notebooks_to_test(args=args)
    assert notebooks == expected


def test_get_notebooks_to_test_with_multiple_dir_paths_with_exclude_files():
    cwd = os.path.dirname(__file__)
    notebook_folders = [
        os.path.join(cwd, "resources"),
        os.path.join(cwd, "resources-2")
    ]
    expected = [os.path.join(cwd, 'resources/unittest_failed.ipynb'),
                os.path.join(cwd, 'resources/runtime_error.ipynb'),
                os.path.join(cwd, 'resources/basic.ipynb'),
                os.path.join(cwd, 'resources-2/a1.ipynb')]
    args = {
        "PATH": list(notebook_folders),
        "--exclude": [os.path.join(cwd, 'resources/doctest_failed.ipynb'),  os.path.join(cwd, 'resources-2/b1.ipynb')],
    }
    notebooks = treon.get_notebooks_to_test(args=args)
    assert notebooks == expected


def test_get_notebooks_to_test_with_multiple_dir_paths_with_exclude_folder():
    cwd = os.path.dirname(__file__)
    notebook_folders = [
        os.path.join(cwd, "resources"),
        os.path.join(cwd, "resources-2")
    ]
    expected = [os.path.join(cwd, 'resources-2/a1.ipynb'),
                os.path.join(cwd, 'resources-2/b1.ipynb')]
    args = {
        "PATH": list(notebook_folders),
        "--exclude": [os.path.join(cwd, 'resources')],
    }
    notebooks = treon.get_notebooks_to_test(args=args)
    assert notebooks == expected