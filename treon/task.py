import traceback

from .test_execution import execute_notebook


class Task:
    def __init__(self, file_path):
        self.file_path = file_path
        self.is_successful = False

    def run_tests(self):
        print("Triggered test for {file_path} \n".format(file_path=self.file_path))

        try:
            is_successful, console_output = execute_notebook(self.file_path)
            result = self.result_string() + console_output + '\n'
            print(result)
        except Exception as ex:
            print(self.error_string(traceback.format_exc()))

    def result_string(self):
        if self.is_successful:
            return '{file_path}       -- PASSED \n'.format(file_path=self.file_path)
        else:
            return '{file_path}       -- FAILED \n'.format(file_path=self.file_path)

    def error_string(self, stack_trace):
        variables = {
            'file_path': self.file_path,
            'stack_trace': stack_trace
        }
        error_string = """
            ERROR in testing {file_path}
            {stack_trace}
            \n
        """.format(**variables)

        return error_string
