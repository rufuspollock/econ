+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Introduction
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This project contains code for economics modelling. Currently the language
of choice is python.

Copyright
*********

Copyright (c) 2004-2006 Open Knowledge Foundation. All rights reserved.

Contributors to the project are listed in AUTHORS.

License
*******

See the file "LICENSE" for the license on this software, including
terms & conditions for usage, and a DISCLAIMER OF ALL WARRANTIES.

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Getting Started
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Dependencies
************

python
======

This package is written in python (http://www.python.org/) and requires a
python version >= 2.3 to function.

mx.Tidy (optional)
===================

econ.data.tabular.HtmlWriter prettyPrint functionality depends on mx.Tidy
package (this functionality is disabled in normal used) 


Installation
************

1. Install Code
===============

Either add the path to ./src to your PYTHONPATH or run:
  $ python setup.py install

2. Confirguation File
=====================

Make a copy the file etc/econ.conf.new and place it somewhere permanent (e.g.
etc/econ.conf). Then open it in your favourite text editor and set any
necessary configuration options.

Finally in any environment from which you which to use the econ package (shell,
webserver etc) you will need to set the ECONCONF variable to point to the
location of this file.

3. Test Installation
====================

You can test your installation by opening a python shell and running:

  >>> import econ
  >>> print econ.__version__


Command Line Admin Utility
**************************

  $ bin/econ-admin

Then follow the instructions to get help


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
For Developers
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Code Layout and Running the Tests 
*********************************

Source files are kept in the src/ tree. Test harnesses are kept side by
side with the classes and functions they test with test or Test
appended to the file name.

  $ bin/econ-test

