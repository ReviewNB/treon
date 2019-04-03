import nbformat
import textwrap
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import new_code_cell


def execute_notebook(path):
    notebook = nbformat.read(path, as_version=4)
    notebook.cells.extend([unittest_cell(), doctest_cell()])
    ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {'path': '.'}})
    return parse_test_result(notebook.cells)


def parse_test_result(cells):
    is_successful, console_output = True, ''
    unittest_output = cells[-2].outputs
    doctest_output = cells[-1].outputs

    if unittest_output:
        has_unittest_passed, unittest_output = parse_unittest_output(unittest_output)
        is_successful = is_successful and has_unittest_passed
        console_output += unittest_output

    if doctest_output:
        has_doctest_passed, doctest_output = parse_doctest_output(doctest_output)
        is_successful = is_successful and has_doctest_passed
        console_output += doctest_output

    return is_successful, console_output


def parse_unittest_output(outputs):
    has_passed, text = False, ''

    for output in outputs:
        text += output.text +  '\n'

    if 'OK' in text[-25:]:
        has_passed = True

    return has_passed, text


def parse_doctest_output(outputs):
    has_passed, text = False, ''

    for output in outputs:
        text += output.text +  '\n'

    if 'Test passed.' in text[-25:]:
        has_passed = True

    return has_passed, text


def unittest_cell():
    source = textwrap.dedent("""
        from IPython.display import clear_output
        import unittest

        r = unittest.main(argv=[''], verbosity=2, exit=False)

        if r.result.testsRun == 0:
            clear_output()
    """)
    return new_code_cell(source=source)


def doctest_cell():
    source = textwrap.dedent("""
        from IPython.display import clear_output
        import doctest

        r = doctest.testmod(verbose=True)

        if r.attempted == 0:
            clear_output()
    """)
    return new_code_cell(source=source)
