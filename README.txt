## Introduction

This project contains economics-related open source and open data material.


## Copyright and License

Copyright (c) 2004-2007 Open Knowledge Foundation. All rights reserved.

All material is available under and open license see the file "LICENSE.txt" for
details.

Contributors to the project are listed in AUTHORS.


## Installation

### Dependencies

  * python. This package is written in python (http://www.python.org/) and
    requires a python version >= 2.3 to function.
  * setuptools (python package)

### Install Code

1. Either: Grab the source code and then run:

  $ sudo python setup.py install

2. OR: use easy_install: $ easy_install econ

### Create Confirguation File

Copy the file etc/econ.ini.new to development.ini and edit to reflect your
setup.

Finally for convenience you may want to set the ECONCONF environment variable to point to the
location of this file.


### Test Installation

You can test your installation by opening a python shell and running:

  >>> import econ
  >>> print econ.__version__


## Command Line Admin Utility

    $ bin/econ-admin

Then follow the instructions to get help


## For Developers

Running tests: we use py.test for running test.

