#  TextSpread
#  Copyright (C) 2013-2014 Robert Iwancz
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
#  test_parse.py
#  


import os
import unittest

from textspread.config import get_parse_config

CUR_DIR = os.path.dirname(__file__)
INPUT_PATH = os.path.join(CUR_DIR, 'input')



class ParseTest(unittest.TestCase):
    """Test parsing."""

    def setUp(self):
        self.pc = get_parse_config(os.path.join(INPUT_PATH, 'simple.yaml'))

    def test_simple(self):
        """Ultra simple case: Single item between ==== delimiters."""
        
        pc = self.pc
        pc.parse()
        self.assertTrue(pc.name == "Simple")
        
        results = pc.result_list
        self.assertTrue(results[0][0] == "text 1")
        self.assertTrue(results[1][0] == "02/02/14 text 2")
        self.assertTrue(results[2][0] == "text 3 line2")
        self.assertTrue(results[3][0] == "text 4 another line paragraph 2")
        self.assertTrue(results[4][0] == "text 5")
        self.assertTrue(results[5][0] == "text 6")
        self.assertTrue(results[6][0] == "text 7")


if __name__ == '__main__':
    unittest.main()
    
