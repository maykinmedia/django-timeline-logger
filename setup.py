#!/usr/bin/env python
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='django-timeline-logger',
    version='0.1a',
    description='Generic event logger for Django models.',
    author='MaykinMedia Team staff',
    author_email='team@maykinmedia.nl',
    url='https://www.maykinmedia.nl',
    install_requires=[
        'Django>=1.7',
    ],
    packages=find_packages(exclude=['tests*']),
    test_suite='tests',
    tests_require=[
        'pytest-django',
        'pytest-cov',
        'pytest-pep8',
        'pytest-pylint',
    ],
    cmdclass={'test': PyTest},
)
