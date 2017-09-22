# RFID

[![Version][version-image]][version-url]
[![License][license-image]][license-url]
[![Build Status][build-image]][build-url]
[![Coverage][coverage-image]][coverage-url]

This Python module provides an interface to communicate with UHPPOTE RFID access control systems.

## Installation

Coming soon.

## Usage

This library can be incorporated in a standard Python format.  A number of controls are made available from the base
library:

```python
from uhppote_rfid import Controller

# Connect to the controller
controller = Controller(
    host='192.168.1.123',
    port=60000,
    serial_number=123456789  # Can be either serial on board or last-4 digits of MAC address
)

# Get the board status
controller.getStatus()

# Remotely open door #1
controller.openDoor(1)
```

Full details of the library's capabilities can be found in the [usage guide][github-usage].

### Dependencies

[Python 2.7][python] and [pip][pip] must be installed prior to use.  Dependencies can be installed using the provided
Makefile:

```bash
make dependencies
```

## Contributing

There are many ways to contribute to this project!  If you have an idea, or have discovered a bug, please
[open an issue][github-issue] so it can be addressed.

If you are interested in contributing to the project through design or development, please read our
[Contribution Guidelines][github-contribute].

### Testing

A `Makefile` is provided to assist with linting, testing, and code coverage generation.  Dependencies will be managed
automatically during testing:

```bash
make test      # Runs linting and test suites
make coverage  # Runs linting, tests, and generates an HTML coverage report
```

## Release Policy

Releases of this project follow [Semantic Versioning][semver] standards in a `MAJOR.MINOR.PATCH`
versioning scheme of the following format:

* `MAJOR` - modified when major, incompatible changes are made to the application,
* `MINOR` - modified when functionality is added in a backwards-compatible manner, and
* `PATCH` - patches to existing functionality, such as documentation and bug fixes.

## License

**This project is in no-way related to the TK company or any subsidiaries.**  Usage of this code may void your
warranty or irreparably damage hardware.  By using this software, you do so at your own risk without any expectation
of support or warranty.

> Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
> an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
> specific language governing permissions and limitations under the License.
>
> By using this software, you agree to free this project,  its owners, and its contributors from any liability.  Do
> not download or use this software unless you fully agree to this project's license and the statements provided here.

This project is made available under the [Apache 2.0 License][github-license].

```
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
```


[version-image]:     http://img.shields.io/badge/release-0.1.0-blue.svg?style=flat
[version-url]:       https://github.com/andrewvaughan/uhppote-rfid/releases
[license-image]:     http://img.shields.io/badge/license-Apache_2.0-blue.svg?style=flat
[license-url]:       https://github.com/andrewvaughan/uhppote-rfid/blob/master/LICENSE
[build-image]:       https://travis-ci.org/andrewvaughan/uhppote-rfid.svg?branch=master
[build-url]:         https://travis-ci.org/andrewvaughan/uhppote-rfid
[coverage-image]:    https://coveralls.io/repos/github/andrewvaughan/rfid/badge.svg?branch=master
[coverage-url]:      https://coveralls.io/github/andrewvaughan/rfid?branch=master

[semver]:            http://semver.org/
[python]:            https://www.python.org/
[pip]:               https://pypi.python.org/pypi/pip

[github-issue]:      https://github.com/andrewvaughan/uhppote-rfid/issues
[github-contribute]: https://github.com/andrewvaughan/uhppote-rfid/blob/master/.github/CONTRIBUTING.md
[github-usage]:      https://github.com/andrewvaughan/uhppote-rfid/master/USAGE.md
[github-license]:    https://github.com/andrewvaughan/uhppote-rfid/blob/master/LICENSE
