# Specification

A "Data Bundle" is a collection of data. A data bundle must consist of at least
one metadata file named metadata.txt and 0 or more data files.

The metadata format follows the standard .ini format as supported by python
ConfigParser (http://docs.python.org/library/configparser.html).

Data files are specified by including sections named after the file. The
default (operating when no files are specified) is for there to be one file
named 'data.csv'.

## Metadata Specification

Possible attributes (*) indicates required.

  * id (*)
  * title (*)
  * license (if not provided defaults to public domain)
  * comments
  * source
  * tags
  * requires-compilation (indicates that bundle must be 'compiled' via running
    a script for example).

### license

(case-insensitive)

Format: value [, value]*. <free-text>

value = mit | cc-by | cc-by-sa | pd | [a-z0-9_-]+

pd = public domain
mit = mit-data / normal mit
