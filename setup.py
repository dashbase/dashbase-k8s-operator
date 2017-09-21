# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='dashbase_operator',
    version='0.1',
    url='http://www.dashbase.io',
    maintainer='Pure White',
    maintainer_email='daniel48@126.com',
    py_modules=['dashops'],
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    install_requires=[
        'click==6.7',
    ],
    entry_points='''
        [console_scripts]
        dashops=dashops.main:root
    ''',
)