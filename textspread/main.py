#!/usr/bin/env python
#
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
#  main.py
#  Application entry point.
#
import sys
import logging

import PySide.QtGui

from textspread import VERSION_STRING, APPLICATION_NAME
from textspread.ui.mainwin import MainWindow


def parse_arguments():
    rv = None
    try:
        import argparse
        
        parser = argparse.ArgumentParser(description= APPLICATION_NAME + ': ' + 
            'Parse data in text files and convert into a tabular format (table/spreadsheet/database,CSV).')
        
        parser.add_argument('-i', '--info', action='store_const',
                            const=logging.INFO, dest='loglevel',
                            help='show info messages.')
        parser.add_argument('-q', '--quiet', action='store_const',
                            const=logging.CRITICAL, dest='loglevel',
                            help='show only critical errors.')
        parser.add_argument('-D', '--debug', action='store_const',
                            const=logging.DEBUG, dest='loglevel',
                            help='show all message, including debug messages.')
                
        parser.add_argument('-v', '--version', 
                            action='version', 
                            version="%s %s" % (APPLICATION_NAME, 
                                               VERSION_STRING))
        
        parser.add_argument('config', nargs='+', help='Configuration filename(s)')
                
        rv = parser.parse_known_args()[0]
    except ImportError:
        # Just forget the whole command line argument parsing thing if
        # running a version of python without argparse :(
        pass

    return rv


def init_logging(level=None):
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:\t%(message)s\t[%(name)s]')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    if level:
        logger.setLevel(level)
        logger.info("Starting %s v%s: setting log level to %d", APPLICATION_NAME, VERSION_STRING, level)
    else:
        logger.info("Starting " + APPLICATION_NAME + " " + VERSION_STRING)


def main():
    loglevel = None
    config_filenames = ['config.yaml',]

    args = parse_arguments()
    if args:
        loglevel = args.loglevel
        config_filenames = args.config
    
    init_logging(loglevel)

    app = PySide.QtGui.QApplication(sys.argv)
    mainwin = MainWindow(config_filenames)
    mainwin.show()
    app.exec_()
