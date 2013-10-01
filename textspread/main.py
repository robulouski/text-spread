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
#  main.py
#  Application entry point.
#
import sys
import PySide.QtGui

from textspread import VERSION_STRING, APPLICATION_NAME
from textspread.ui.mainwin import MainWindow
import textspread.config



def main():
    try:
        import argparse
        parser = argparse.ArgumentParser(description= APPLICATION_NAME + ': ' + 
            'Parse text files into tables.')
        parser.add_argument('-v', '--version', 
                            action='version', 
                            version="%s %s" % (APPLICATION_NAME, 
                                               VERSION_STRING))
        parser.parse_known_args()
    except ImportError:
        # Just forget the whole command line argument parsing thing if
        # running a version of python without argparse :(
        pass

    plist = textspread.config.get_parse_config()
    
    app = PySide.QtGui.QApplication(sys.argv)
    mainwin = MainWindow(plist)
    mainwin.show()
    app.exec_()
