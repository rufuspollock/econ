+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Introduction
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This project contains code for economics modelling. Currently the language
of choice is python. Please see the AUTHORS file for contributors and the
COPYING file for copyright and licence details.

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

This package is written in python (http://www.python.org/) and requires a
python version >= 2.3 to function.

configobj
=========

We use the voidspace configobj package. Please make sure that configobj is on
the path (import configobj should work from a python shell).

mx.Tidy (optional)
===================

HtmlTableWriter prettyPrint functionality depends on mx.Tidy package.

Confirguation File
******************

Make a copy the file etc/econ.conf.new and place it somewhere permanent (e.g.
etc/econ.conf). Then open it in your favourite text editor and set any
necessary configuration options.

Finally in any environment from which you which to use the econ package (shell,
webserver etc) you will need to set the ECONCONF variable to point to the
location of this file.

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

To get started try running all the tests by doing (you may need to
first install additional libraries -- see Library Dependencies below):

$ cd test
$ python main.py test

It is suggested that you create your own local copy of main.py called,
say, main_<username>.py and modify this. DO NOT COMMIT any changes of
main.py to the repository OR ADD your own copy of main.py.

