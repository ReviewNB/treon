# -*- encoding: utf-8 -*-
import contextlib
import pathlib

from treon.treon import build_ignore_list


TEST_NOTEBOOK_PATH = pathlib.Path(__file__).parent.joinpath('resources')


@contextlib.contextmanager
def _temporary_treonignore(*rules):
    ignorefile = TEST_NOTEBOOK_PATH.joinpath('.treonignore')
    try:
        ignorefile.touch(exist_ok=False)
        ignorefile.write_text('\n'.join(rules))
        yield
    finally:
        ignorefile.unlink()


def test_no_ignore():
    with _temporary_treonignore():
        assert build_ignore_list(TEST_NOTEBOOK_PATH) == []

def test_path_ignore():
    with _temporary_treonignore('basic.ipynb'):
        ignored = build_ignore_list(TEST_NOTEBOOK_PATH)
        assert len(ignored) == 1
        assert TEST_NOTEBOOK_PATH.joinpath('basic.ipynb').samefile(ignored[0])


def test_path_ignore_absolute():
    with _temporary_treonignore('/basic.ipynb'):
        ignored = build_ignore_list(TEST_NOTEBOOK_PATH)
        assert len(ignored) == 1
        assert TEST_NOTEBOOK_PATH.joinpath('basic.ipynb').samefile(ignored[0])


def test_glob_ignore():
    with _temporary_treonignore('*'):
        ignored = build_ignore_list(TEST_NOTEBOOK_PATH)
        assert len(ignored) == len(list(TEST_NOTEBOOK_PATH.iterdir()))
