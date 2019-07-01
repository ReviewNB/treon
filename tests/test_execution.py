# -*- encoding: utf-8 -*-
import os
import pytest

from nbconvert.preprocessors import CellExecutionError
from treon.test_execution import execute_notebook


def test_successful_execution():
    successful, _ = _run('resources/basic.ipynb')

    assert successful


def test_failed_execution():
    with pytest.raises(CellExecutionError) as exc_info:
        _run('resources/runtime_error.ipynb')

    assert 'ZeroDivisionError' in exc_info.value.traceback


def test_failed_unittest():
    successful, output = _run('resources/unittest_failed.ipynb')

    assert not successful
    assert 'AssertionError' in output


def test_failed_doctest():
    successful, output = _run('resources/doctest_failed.ipynb')

    assert not successful
    assert 'Test Failed' in output


def _run(notebook):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), notebook)
    return execute_notebook(path)
