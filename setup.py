#!/usr/bin/env python
import sys

from setuptools import setup, find_packages


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
)
