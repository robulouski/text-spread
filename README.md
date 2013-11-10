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

