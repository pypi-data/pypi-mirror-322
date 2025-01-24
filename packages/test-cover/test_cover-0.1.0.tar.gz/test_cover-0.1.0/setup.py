#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
===============================
test_cover
===============================


.. image:: https://img.shields.io/pypi/v/test_cover.svg
        :target: https://pypi.python.org/pypi/test_cover

.. image:: https://img.shields.io/travis/usalko/test_cover.svg
        :target: https://travis-ci.org/usalko/test_cover



HtmlTest runner is a unittest test runner that save test results
in Html files, for human readable presentation of results.

This Package is a fork ``html-testRunner``.

Usage:
--------------

.. code-block:: python

    import test_cover
    import unittest


    class TestStringMethods(unittest.TestCase):

        def test_upper(self):
            self.assertEqual('foo'.upper(), 'FOO')

        def test_error(self):
            "\"" This test should be marked as error one. ""\"
            raise ValueError

        def test_fail(self):
            "\"" This test should fail. ""\"
            self.assertEqual(1, 2)

        @unittest.skip("This is a skipped test.")
        def test_skip(self):
            "\"" This test should be skipped. ""\"
            pass

    if __name__ == '__main__':
        unittest.main(testRunner=test_cover.HtmlTestRunner(output='example_dir'))

As simple as import the class an initialize it, it only have one request
parameter that is output, this one is use to place the report in a sub
direcotry in ``reports`` directory.

Links:
---------

* `Github <https://github.com/usalko/test_cover>`_
"""

from setuptools import setup

requirements = [
    # Package requirements here
    "Jinja2>=2.10.1"
]

test_requirements = [
    # Package test requirements here
]

setup(
    name='test_cover',
    version='0.1.0',
    description="A Test Runner in python, for Human Readable HTML Reports",
    long_description=__doc__,
    author='usalko',
    author_email='ivict@rambler.ru',
    url='https://github.com/usalko/test_cover',
    packages=[
        'test_cover',
    ],
    package_dir={'test_cover':
                 'test_cover'},
    include_package_data=True,
    install_requires=requirements,
    license='APACHE 2.0',
    zip_safe=False,
    keywords='test_cover TestRunner Html Reports',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
