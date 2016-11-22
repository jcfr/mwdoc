#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import versioneer

with open('README.md', 'r') as fp:
    readme = fp.read()

with open('requirements.txt', 'r') as fp:
    requirements = list(filter(bool, (line.strip() for line in fp)))

with open('requirements-dev.txt', 'r') as fp:
    dev_requirements = list(filter(bool, (line.strip() for line in fp)))

setup(
    name='mwdoc',

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    author='Jean-Christophe Fillion-Robin',
    author_email='jchris.fillionr@kitware.com',

    url='https://github.com/jcfr/mwdoc#readme',

    description='Allow to easily version mediawiki pages.',
    long_description=readme,

    packages=['mwdoc'],
    package_data={},
    include_package_data=True,
    zip_safe=False,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],

    license="Apache",

    keywords='mediawiki wikipedia',

    install_requires=requirements,
    tests_require=dev_requirements,
)
