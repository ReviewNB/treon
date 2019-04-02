import nbformat
import traceback
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.reader import NotJSONError


def execute_notebook(path):
    notebook = nbformat.read(path, as_version=4)
    ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {'path': '.'}})
    print(path + '                          -- PASSED')

def run(notebooks):
    for notebook in notebooks:
        print("Running sanity test for " + notebook)

        try:
            execute_notebook(notebook)
        except NotJSONError as ex:
            print("ERROR in sanity test for {notebook}".format(notebook=notebook))
            print(traceback.format_exc())

