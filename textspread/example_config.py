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
#  example_config.py
#

import textspread.parse_config


def example_parse_config( ):
    
    plist = []

    p = textspread.parse_config.ParseConfig("Stock Tips")
    p.filepath = "C:/path/to/input_file.txt"
    p.column_list = ["Stock","Direction","Open Date",
             "Open Price","Rec Limit Price","Rec Stop Loss",
             "Rec Trailing Stop","Closed Date","Close Price",
             "Market Price","Stop Loss","Stop Distance", "Risk Amount","Qty to Buy",
             "Position Amount","Notes","Pad1", "Pad2", "Name"
             ]
    p.header_column_index = 2
    p.main_regex = r'(A.*?(?:Portfolio|Report).*?(?:buy|sell).*?(unit|stop).*?)(?:\n\n|$)'
    p.add_extract(r'\s*(buy|sell)\w*\s+\d+,?\d*(?:\s+units)?(?:\s+of)?\s+(.*?)\((\w+)\)(?:.*?(?:up|down)\s*to\s*\$(\d+\.*\d*))?',
                        ((1, 1),
                         (2, 18),
                         (3, 0),
                         (4, 4),
                         (4, 9)
                         ),
                         (
                          (1, (('buy', 'LONG'), ('sell', 'SHORT'))),
                         )
                        )   
    p.add_extract(r'.*?Stop(?:\s*loss)?(?:\s*is)?(?:\s*at)?\s+\$(\d+\.?\d*)',
                  ((1, 5),(1,10))
                  )
    p.add_extract(r'\[ent.*?\$?(\d+\.*\d*)',
                  ((1, 3),)
                  )    
    p.parse()
    plist.append(p)

    return plist

