import logging
import textwrap

from nbconvert.preprocessors import CellExecutionError
from nbconvert.utils.exceptions import ConversionException

from .test_execution import execute_notebook

LOG = logging.getLogger('treon.task')


def _is_verbose():
    return LOG.isEnabledFor(logging.DEBUG)


class Task:
    def __init__(self, file_path, html):
        self.file_path = file_path
        self.is_successful = False
        self.html = html

    def run_tests(self):
        LOG.info("Triggered test for %s", self.file_path)

        try:
            self.is_successful, console_output = execute_notebook(self.file_path, self.html)
            result = self.result_string()

            if not self.is_successful or _is_verbose():
                result += console_output

            LOG.info(result)
        except CellExecutionError as cell_error:
            LOG.error(self.error_string(cell_error.traceback))
        except ConversionException:
            LOG.exception("Execution of notebook '%s' failed", self.file_path)

    def result_string(self):
        if self.is_successful:
            return '\n{file_path}     -- PASSED \n'.format(file_path=self.file_path)

        return '\n{file_path}     -- FAILED \n'.format(file_path=self.file_path)

    def error_string(self, stack_trace):
        variables = {
            'file_path': self.file_path,
            'stack_trace': stack_trace
        }
        error_string = textwrap.dedent("""\
            ERROR in testing {file_path}
            
            {stack_trace}
            \n
        """).format(**variables)

        return error_string
