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


from setuptools import setup


def readme():
    """
    Attempts to convert the README file to rst format and return it.
    """
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst').decode('utf-8')
    except (ImportError, OSError):
        return open('README.md', 'rb').read().decode('utf-8')


def license():
    """
    Returns text from the LICENSE file.
    """
    return open('LICENSE', 'rb').read().decode('utf-8')


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
    install_requires=[]
)
