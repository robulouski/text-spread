TextSpread
==========

An attempt at a general purpose solution to the problem of extracting data
from (reasonably well formatted) text files and presenting that data in a
tabular format (i.e. spreadsheet).

The basic idea is that there will be config file(s) which specify 
filename(s) along with regexes and options for how the file(s) should be 
parsed, and into which column data extracted with the regexes should go.  
Once parsed a simple GUI displays the extracted data in table widgets (on 
a separate tab for each file), with the possibility from there to copy and
paste selectively, or save the whole thing as a CVS file, spreadsheet, etc.

Written in Python with PySide Qt bindings.


Motivation
----------

There are text file(s).  They contain data, somewhat freeform, but orderly
enough that parsing with regular expressions is workable.

You desire to extract said data into another, more tabular form --
spreadsheet, database, CSV file, etc

The data is in "chunks".  Each chunk is delimited by a line with a certain
pattern of characters (i.e. something that can be represented by a regex,
and will not be confused with actual chunk data).

A chunk may represent an individual "record".  Alternatively, a single
chunk may contain multiple discrete items of data that need to be split up
first (based on a different delimiter).  Both cases can be accommodated.

For the sake of consistent terminology, we will say that an input file
contains "chunks" of data, separated by a delimiter (specified by the
chunk-regex).  A chunk may contain one or more "items" of data, separated
by an item delimiter (item-regex).  If an item-regex is not specified, it's
assumed chunks will only contain a single item of data.

Chunks may (optionally) contain header data, that applies to every item in
the chunk.  (For example, chunks could consist of items for a particular
date, the first line of the chunk being the date, which applies to all
items in that chunk.)

The goal of TextSpread is to provide the ability to parse and extract data
from such files by writing a simple YAML configuration file -- instead of
having to write/modify bespoke scripts with lots of boilerplate code.


Quick start
-----------

Consider an ultra-simple use case.

You have a text file.  It contains data.  Each chunk of data is separated
by a line of '=' (equal) characters.  Let's say that a line of 4 or more
equal characters will constitute a record separator.

To parse this file, extracting the text between separators, create a YAML
config file.  Let's call it ``simple.yaml``::

  ---
  name: Simple
  filename: testdata/simple.txt
  columns: ["Data",]
  chunk-delimiter: '\s*====+\s*'
  extract:
    - regex: '(.*)'
      mappings: 
        - [1, 0]
  output: GUI


Run TextSpread with this config file::

  ./text_spread.py simple.yaml

This will display a table with one column (index 0) containing the match
from group 1 in the regular expression, which in this case grabs
everything in the chunk.



Random Notes
------------

* JSON configuration files largely untested at this stage.
* Newlines between chunks/records are stripped.
* Searches are case insensitive.
* Copy and paste from the results table grid works using the ususal 
  keyboard shortcuts. (Menu options coming soon)


Configuration Options
---------------------

Each configuration file specified on the command line must be a valid YAML
file (or JSON, but be sure to escape the regexes properly).  Each config
file defines settings that specify the input source, how that input
source should be parsed, and where the output should go.  If output is the
GUI, each config file defines contents of a table that will be displayed on
it's own tab.

The following sections describe the various settings.


Compulsory Configuration Settings
---------------------------------

The following settings must appear in each configuration file.

``name``
  Identifier of output.  If outputting to the GUI, it will be the label of
  the Tab Widget.  If output is a database, this must be the name of the
  target table.  If output is a file, this must be the full valid file
  path.

``filename``
  Input filename.

``columns``
  An array of column/field names.  Each value must be a string.  If output
  is the GUI or CSV, these will constitute values for the heading row.  If
  output is a database, these must be valid field names for the table
  specified in ``name``.

``chunk-delimiter``
  Regular expression that specifies the delimiter between chunks of data.

``extract``
  Defines the data to be extracted from each item.  Must contain the 
  following:

  - ``regex``: A regular expression, including parenthesized groups.
  
  - ``mappings``: A list of mappings between groups captured by the above
    regular expression, and column indexes where the results will be
    stored.  Each element of the list must be a 2 element list:
    ``[group-number, column-index]``

    For example, a mappings value of ``[[1,0], [2,1]]`` means that group 1
    matched by the regex corresponds to the output value of column index 0,
    and group 2 corresponds to column index 1.

    ``subs``: Optional substitutions.  If present, facilitates simple
    search-and-replace actions on matched data.  Must be a list where each
    element contains the following:

    - ``index``: Index of results on which to attempt the substitution.

    - ``replacements``: A list that specifies the substitutions.  Each item
      must be a 2 element list [a, b] where a is the text to search for,
      and b is the replacement text.    



Optional Configuration Settings
-------------------------------

``item-delimiter``
  If specified, any matching lines within a chunk will split the chunk into
  multiple items.  (Otherwise, a chunk will consist of a single item.)

``filter`` 
  Optional regular expression, if specified any items NOT matching will be
  skipped.

``header``
  An object defining header data, that if present will apply to every item
  in the chunk.  Must contain the following values:

  ``regex``: Regular expression that will match header lines.  (Only the
  first line that matches will be the header.)

  ``index``: Index of results array where the matching header line will be
  stored.



Author
------

| Robert Iwancz
| www.voidynullness.net
| ``@robulouski``

