[![PyPI version](https://badge.fury.io/py/treon.svg)](https://badge.fury.io/py/treon)

# treon
Easy to use test framework for Jupyter Notebooks.
* Runs notebook top to bottom and flags execution errors if any
* Runs [unittest](https://docs.python.org/2/library/unittest.html) present in your notebook code cells
* Runs [doctest](https://docs.python.org/2/library/doctest.html) present in your notebook code cells

### Why should you use it?
* Start testing notebooks without writing a single line of code
* Multithreaded execution for quickly testing a set of notebooks
* Executes every Notebook in a fresh kernel to avoid kernel state interference
* Primarily a command line tool that can be used easily in any Continuous Integration (CI) system
* Soon to be part of [ReviewNB](https://www.reviewnb.com/)'s CI system that automatically runs treon everytime you push notebook changes to GitHub


## Installation
```
pip install treon
```

## Usage
```
$ treon
Executing treon version 0.1.0
Recursively scanning /workspace/treon/tmp/docs/site/ru/guide for Notebooks...

-----------------------------------------------------------------------
Collected following Notebooks for testing
-----------------------------------------------------------------------
/workspace/treon/tmp/docs/site/ru/guide/keras.ipynb
/workspace/treon/tmp/docs/site/ru/guide/eager.ipynb
-----------------------------------------------------------------------

Triggered test for /workspace/treon/tmp/docs/site/ru/guide/keras.ipynb
Triggered test for /workspace/treon/tmp/docs/site/ru/guide/eager.ipynb

test_sum (__main__.TestNotebook) ...
ok
test_sum (__main__.TestNotebook2) ...
ok
test_sum (__main__.TestNotebook3) ...
ok

----------------------------------------------------------------------
Ran 3 tests in 0.004s

OK

-----------------------------------------------------------------------
TEST RESULT
-----------------------------------------------------------------------
/workspace/treon/tmp/docs/site/ru/guide/keras.ipynb       -- PASSED
/workspace/treon/tmp/docs/site/ru/guide/eager.ipynb       -- PASSED
-----------------------------------------------------------------------
2 succeeded, 0 failed, out of 2 notebooks tested.
-----------------------------------------------------------------------
```

## Command line arguments
```
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

```

## unitttest example
You just need to add tests as shown below & treon would execute them and report the result on the console. See [this](https://docs.python.org/2/library/unittest.html) for more details on how to write unittest.

![](images/unittest.png)

## doctest example
You just need to add tests as shown below & treon would execute them and report the result on the console. See [this](https://docs.python.org/2/library/doctest.html) for more details on how to write doctest.

![](images/doctest.png)

## Note about dependencies
* You need to run treon from environment (virtualenv/pipenv etc.) that has all the dependcies required for Notebooks under test
* treon only works with python3+ environments and uses python3 kernel for executing notebooks

## Development
For development, you may use below to create a Python interpreter that resides in `venv` in the current working directory, and to install all of treon's dependencies:

```
$ virtualenv venv 
$ source venv/bin/activate
$ pip install -e .
$ pip install -r requirements-dev.txt
$ treon --help # should work
```

Because the script installs the package as editable, you can make changes in the source tree and use the `treon` command to immediately validate them. If this does not appear to work, check that you are using a the proper virtual environment, and that the package is indeed installed in editable mode:

```
$ which treon # should point into your virtualenv
/path/to/my/venv/bin/treon
$ pip list --local | grep treon # should point to the source tree
treon                0.1.2                /workspace/treon
```

Please refer to the `Makefile` for supplementary development tasks, such as linting treon's source code.
For instance, to run the linter before committing, invoke `make lint`. 

## Motivation
Our aim at [ReviewNB](https://www.reviewnb.com/) is to make notebooks a first class entity in the production workflow. We've built a code review system for Notebooks. The next step is to [build a CI pipeline](https://github.com/ReviewNB/support/issues/19) & treon is the core tool in that effort. It is licensed librerally (MIT) & I foresee it being used as an independent tool as well. You can use it locally and/or integrate with CI system of your choice.

For motivation, checkout [Netflix's blog](https://medium.com/netflix-techblog/scheduling-notebooks-348e6c14cfd6) to see how notebooks are graduating from scratchpad to a part of production workflow.

## Contribute
If you see any problem, open an issue or send a pull request. You can write to team@reviewnb.com for any questions.
