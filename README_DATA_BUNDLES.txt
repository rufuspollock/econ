# Specification

Data bundles is a collection of data. A data bundle must consist of at least one metadata file named metadata.txt and 0 or more data files.

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
