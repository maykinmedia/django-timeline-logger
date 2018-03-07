#!/usr/bin/env python

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-timeline-logger',
    version='0.8.0',
    description='Generic event logger for Django models.',
    long_description=long_description,
    author='Maykin Media',
    author_email='support@maykinmedia.nl',
    url='https://github.com/maykinmedia/django-timeline-logger',
    install_requires=[
        'Django>=1.10',
        'django-appconf',
    ],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=[
        'factory-boy',
        'psycopg2',
        'pytest',
        'pytest-cov',
        'pytest-django',
        'pytest-pep8',
        'pytest-pylint',
        'pytest-pythonpath',
        'pytest-runner',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ]
)
