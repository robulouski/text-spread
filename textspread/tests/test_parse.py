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

from textspread.config import get_parse_config, get_parse_list

CUR_DIR = os.path.dirname(__file__)
INPUT_PATH = os.path.join(CUR_DIR, 'input')



# class ParseTest(unittest.TestCase):
#     """Test parsing."""
# 
#     def setUp(self):
#         files = [os.path.join(INPUT_PATH, f) for f in ('simple.yaml', 'simple_date.yaml')]
#         self.pc_list = get_parse_list(files)


class SimpleTest(unittest.TestCase):
    def runTest(self):
        """Ultra simple case: Single item between ==== delimiters."""

        pc =  get_parse_config(os.path.join(INPUT_PATH, 'simple.yaml'))
        self.assertTrue(pc.name == "Simple")
        pc.parse()
        
        results = pc.result_list
        self.assertTrue(results[0][0] == "text 1")
        self.assertTrue(results[1][0] == "02/02/14 text 2")
        self.assertTrue(results[2][0] == "text 3 line2")
        self.assertTrue(results[3][0] == "text 4 another line paragraph 2")
        self.assertTrue(results[4][0] == "text 5")
        self.assertTrue(results[5][0] == "text 6")
        self.assertTrue(results[6][0] == "text 7")


class SimpleDateTest(unittest.TestCase):
    def runTest(self):
        """Bit more complex: Multiple items between ==== delimiters, date header."""

        pc =  get_parse_config(os.path.join(INPUT_PATH, 'simple_date.yaml'))
        self.assertTrue(pc.name == "Simple Date")
        pc.parse()
        
        results = pc.result_list
#        print results
        self.assertEqual(results[0][0], "01/02/14")
        self.assertEqual(results[0][1], "item 1")
        self.assertEqual(results[1][0], "02/02/14")
        self.assertEqual(results[1][1], "item 2")
        self.assertEqual(results[2][0], "03/02/14")
        self.assertEqual(results[2][1], "item 3 line2")
        self.assertEqual(results[3][0], "03/02/14")
        self.assertEqual(results[3][1], "item 4")
        self.assertEqual(results[4][0], "04/02/14")
        self.assertEqual(results[4][1], "item 5 another line another paragraph")
        self.assertEqual(results[5][0], "04/02/14")
        self.assertEqual(results[5][1], "item 6 another line another paragraph")
        self.assertEqual(results[6][0], "04/02/14")
        self.assertEqual(results[6][1], "item 7 another line another paragraph")
        self.assertEqual(results[7][0], "05/02/14")
        self.assertEqual(results[7][1], "item 8")
        self.assertIsNone(results[8][0])
        self.assertEqual(results[8][1], "item 9")
        self.assertIsNone(results[9][0])
        self.assertEqual(results[9][1], "item 10")
        self.assertIsNone(results[10][0])
        self.assertEqual(results[10][1], "item 11")
        self.assertEqual(results[11][0], "06/02/14")
        self.assertEqual(results[11][1], "item 12")



class StocksTest(unittest.TestCase):
    def runTest(self):
        """Test filter and substitutions."""

        pc =  get_parse_config(os.path.join(INPUT_PATH, 'stocks.yaml'))
        self.assertTrue(pc.name == "Stocks")
        pc.parse()
        
        results = pc.result_list
#        print results
        expected = [
                    ['AAA',  'NYSE',   'LONG',  '16/01/2013'],
                    ['BBB',  'NYSE',   'SHORT', '17/01/2013'],
                    ['ZZZZ', 'NASDAQ',  None,   '18/01/2013'],
                    ['CCC',  'NYSE',   'LONG',  '29/01/2013'],
                    ['DDDD', 'NASDAQ', 'LONG',  '29/01/2013'],
                    ['EEEE', 'NASDAQ', 'SHORT', '29/01/2013'],
                    ]
        self.assertEqual(results[0], expected[0])
        self.assertEqual(results[1], expected[1])
        self.assertEqual(results[2], expected[2])
        self.assertEqual(results[3], expected[3])
        self.assertEqual(results[4], expected[4])
        self.assertEqual(results[5], expected[5])
        
        
if __name__ == '__main__':
    unittest.main()

