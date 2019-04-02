# -*- coding: utf-8 -*-


__version__ = "0.1.0"


import sys
import os
import glob

from .sanity import run as trigger_sanity_tests

def main():
    print("Executing treon version %s." % __version__)
    print("List of argument strings: %s" % sys.argv[1:])
    cwd = os.getcwd()
    print("Recursively scanning {cwd} for Notebooks...".format(cwd=cwd))
    glob_path = cwd + '/**/*.ipynb'
    all_notebooks = glob.glob(glob_path, recursive=True)
    trigger_sanity_tests(all_notebooks)
