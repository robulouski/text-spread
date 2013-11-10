#!/usr/bin/env python
#
#  TextSpread
#  Copyright (C) 2013 Robert Iwancz
#
#  This file is part of TextSpread.
#
#  TextSpread is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  TextSpread is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with TextSpread.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################
#
#  config.py
#
#  Read/parse config files, initialise ParseConfig arrays.
#  TODO: 
#   - Read all this from config file(s)
#


def get_parse_config( ):
    """Read config file(s).  Returns list of ParseConfig objects.

       TODO: read all this from config file
    
    """
    
    parse_func = None
    
    try:
        import textspread.asr_config
        parse_func = textspread.asr_config.asr_parse_config
    except ImportError:
        import textspread.example_config
        parse_func = textspread.example_config.example_parse_config

    return parse_func()

