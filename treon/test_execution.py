import nbformat

from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.reader import NotJSONError


def execute_notebook(path):
    notebook = nbformat.read(path, as_version=4)
    ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {'path': '.'}})
    return True, ''
