#!/usr/bin/env python
"""
Control module for UHPPOTE RFID access-control boards.

https://github.com/andrewvaughan/uhppote-rfid

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


VERSION = '0.1.0'


class LintDocstringCommand(distutils.cmd.Command):
    """
    A custom command to run docstring linting on all Python source files.

    .. versionadded:: 0.1.0
    """

    description = 'run docstring linting on all Python source files'
    user_options = [
        ('explain', 'e', 'show PEP257 and source code upon failure (default: off)'),
        ('debug', 'd', 'show extra debug information (default: off)'),
        ('quiet', 'q', 'return only error count and an error code (default: off)')
    ]

    def initialize_options(self):
        """
        Set up defaults for the command options.

        .. versionadded:: 0.1.0
        .. function:: initialize_options()
        """
        self.explain = False
        self.debug = False
        self.quiet = False


    def finalize_options(self):
        """
        Parse command options prior to running.

        .. versionadded:: 0.1.0
        .. function:: finalize_options()
        """
        pass


    def run(self):
        """
        Execute the LintDocstring command.

        .. versionadded:: 0.1.0
        .. function:: run()
        """
        command = ['/usr/bin/env', 'pydocstyle']

        if self.quiet:
            command.append('--count')

        elif self.explain:
            command.append('--explain')
            command.append('--source')

        if self.debug:
            command.append('--debug')
            command.append('--verbose')

        command.append("%s/" % os.getcwd())

        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.DEBUG
        )

        subprocess.check_call(command)




class LintCommand(distutils.cmd.Command):
    """
    A custom command to run linting on all Python source files.

    .. versionadded:: 0.1.0
    """

    description = 'run code linting on source files'
    user_options = [
        ('explain', 'e', 'show PEP8 and source code upon failure (default: off)'),
        ('quiet', 'q', 'return only error count and an error code; prevents verbosity (default: off)')
    ]


    def initialize_options(self):
        """
        Set up defaults for the command options.

        .. versionadded:: 0.1.0
        .. function:: initialize_options()
        """
        self.explain = False
        self.quiet = False


    def finalize_options(self):
        """
        Parse command options prior to running.

        .. versionadded:: 0.1.0
        .. function:: finalize_options()
        """
        pass


    def run(self):
        """
        Execute the Lint command.

        .. versionadded:: 0.1.0
        .. function:: run()
        """
        command = ['/usr/bin/env', 'pycodestyle']

        if self.quiet:
            command.append('--count')

        elif self.explain:
            command.append('--show-pep8')
            command.append('--show-source')

        command.append("%s/" % os.getcwd())

        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.DEBUG
        )

        subprocess.check_call(command)


def readme():
    """
    Attempt to convert the README file to .rst format and return it.

    .. versionadded:: 0.1.0
    .. function:: readme()
    """
    # try:
    #     import pypandoc
    #     return pypandoc.convert('README.md', 'rst').decode('utf-8')
    # except (ImportError, OSError):
    #     return open('README.md', 'rb').read().decode('utf-8')

    return ""


setup(
    name='UHPPOTE_RFID',
    version=VERSION,
    description='Interface for UHPPOTE RFID control systems.',
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
    keywords='rfid access security for UHPPOTE RFID control boards',
    url='http://github.com/andrewvaughan/uhppote-rfid',
    author='Andrew Vaughan',
    author_email='hello@andrewvaughan.io',
    license='ASL',
    packages=['uhppote_rfid'],
    install_requires=[],
    cmdclass={
        'lint': LintCommand,
        'lint_docstring': LintDocstringCommand,
    }
)
