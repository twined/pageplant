# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='pageplant',
    version='1.0.1',
    author=u'Twined',
    author_email='www.twined.net',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/twined/pageplant',
    license='Do what thou wilt.',
    description='Page generator for twined apps',
    long_description=open('README.md').read(),
    install_requires=[
        "django-reversion >= 1.8.4",
        "django-classy-tags",
        "django-mptt",
    ],
    zip_safe=False,
)
