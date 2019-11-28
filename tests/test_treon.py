from treon import treon


def test_filter_results():
    args = {
        "--exclude": ['resources/basic.ipynb',
                      'failed']
    }
    results = ['resources/basic.ipynb',
               'resources/doctest_failed.ipynb',
               'resources/runtime_error.ipynb',
               'resources/unittest_failed.ipynb',
               'other/resources.ipynb']

    filtered = treon.filter_results(results=results, args=args)
    expected = ['resources/doctest_failed.ipynb',
                'resources/runtime_error.ipynb',
                'resources/unittest_failed.ipynb',
                'other/resources.ipynb']
    assert filtered == expected

    args = {
        "--exclude": ['resources']
    }

    filtered = treon.filter_results(results=results, args=args)
    expected = ['other/resources.ipynb']
    assert filtered == expected

    results = ['resources/basic.ipynb']
    filtered = treon.filter_results(results=results, args=args)
    expected = []
    assert filtered == expected
