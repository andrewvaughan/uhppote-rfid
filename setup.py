#!/usr/bin/env python

"""
RFID
https://github.com/andrewvaughan/rfid

Copyright 2017 Andrew Vaughan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import distutils.cmd
import distutils.log
import os
import setuptools
import subprocess

from setuptools import setup


class LintCommand(distutils.cmd.Command):
    """
    A custom command to run linting on all Python source files.
    """

    description = 'run linting on Python source files'
    user_options = [
        ('verbose', None, 'show PEP8 and source code upon failure (default: off)'),
        ('quiet', None, 'return only error count and an error code (default: off)'),
        ('max-length=', None, 'limit the maximum length of output (default: 118)')
    ]

    def initialize_options(self):
        """
        Sets up defaults for the command options.
        """

        self.verbose = False
        self.quiet = False
        self.max_length = 118

    def finalize_options(self):
        """
        Parses command options prior to running.
        """

        assert self.max_length > 0, 'Maximum length must be greater than 0.'

    def run(self):
        """
        Run the command.
        """

        command = ['/usr/bin/env', 'pycodestyle']

        if self.verbose:
            command.append('--show-pep8')
            command.append('--show-source')

        if self.quiet:
            command.append('--count')

        if self.max_length:
            command.append('--max-line-length=%d' % self.max_length)

        command.append("%s/setup.py" % os.getcwd())

        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO
        )

        subprocess.check_call(command)


def readme():
    """
    Attempts to convert the README file to rst format and return it.
    """

    # try:
    #     import pypandoc
    #     return pypandoc.convert('README.md', 'rst').decode('utf-8')
    # except (ImportError, OSError):
    #     return open('README.md', 'rb').read().decode('utf-8')

    return ""


setup(
    name='rfid',
    version='0.1',
    description='Interface for TK RFID control systems.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Topic :: Home Automation',
        'Topic :: Security',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: Utilities',
    ],
    keywords='rfid access security',
    url='http://github.com/andrewvaughan/rfid',
    author='Andrew Vaughan',
    author_email='hello@andrewvaughan.io',
    license='ASL',
    packages=['rfid'],
    install_requires=[],
    cmdclass={
        'lint': LintCommand
    }
)
