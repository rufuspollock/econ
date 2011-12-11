## Deprecation Notice

The code and data here is no longer actively maintained. The material here was developed primarily from 2005-2009 and powered <http://openeconomics.net/> until July 2011 -- the point at which <http://openeconomics.net/> became the home of the [Open Knowledge Foundation's Economics Working Group](http://economics.okfn.org/).

From July 2011 until November 2011 it was located at <http://old.openeconomics.net/>. It was finally shut down in November 2011. You can see what the site used to look like using the WayBack machine at: <http://web.archive.org/web/20110109091529/http://openeconomics.net/>

While this part of the Open Economics project is now retired much of its work lives on elsewhere in various forms:

* All the data is being converted to individual datasets on the [DataHub](http://github.com/okfn/openspendingjs): <http://thedatahub.org/group/open-economics>
* Much of the code, and especially the larger apps, have merged into [OpenSpending](http://openspending.org/) and [OpenSpendingJS](http://github.com/okfn/openspendingjs) or into [CKAN](http://ckan.org/)
* Many of the data 'bundle' ideas live on in the concept of [data packages](http://www.dataprotocols.org/en/latest/packages.html) and the [data package manager](http://www.dataprotocols.org/en/latest/packages.html#data-package-manager).

## Introduction

This project contains economics-related open source and open data material.

## Contributors, Copyright and License

Contributors to the project are listed in AUTHORS. All code, content and data in Open Economics is open and can be freely used, reused and redistributed. Details of the exact licensing are provided below.

### Code

All code is available under the MIT License:

Copyright (c) 2005-08, Open Knowledge Foundation

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Content and Data

Unless otherwise stated all content and data is licensed under a Creative Commons Attribution license v3.0 (unported + all jurisdictions) with the additional provision that this license should be read broadly to cover not only copyright but also all other IP rights present in this material including, for example, any database rights.

The full text of this license may be found via the following url:

<http://creativecommons.org/licenses/by-sa/3.0/legalcode>


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

Run the following command (where <ini_file> is the name of the configuration
file to be generated):

    $ paster make-config econ <ini_file>

Finally for convenience you may want to set the ECONCONF environment variable
to point to the location of this file.

### Test Installation

You can test your installation by opening a python shell and running:

  >>> import econ
  >>> print econ.__version__


## Command Line Admin Utility

    $ bin/econ-admin

Then follow the instructions to get help


## For Developers

Running tests: we use py.test for running tests.

