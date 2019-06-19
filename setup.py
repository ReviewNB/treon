try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('treon/treon.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "treon",
    packages = ["treon"],
    python_requires='>=3',
    entry_points = {
        "console_scripts": ['treon = treon.treon:main']
    },
    version = version,
    description = "Testing framework for Jupyter Notebooks",
    long_description = long_descr,
    long_description_content_type="text/markdown",
    author = "Amit Rathi",
    author_email = "amit@reviewnb.com",
    url = "https://github.com/reviewNB/treon",
    license='MIT',
    keywords=['test', 'jupyter', 'notebook', 'jupyter test', 'notebook test', 'unittest', 'doctest'],
    install_requires=[
        'nbconvert',
        'jupyter_client',
        'jupyter',
        'docopt'
    ]
    )
