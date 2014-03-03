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
#  config.py
#
#  Read/parse config files, initialise ParseConfig arrays.
#  TODO: 
#   - Read all this from config file(s)
#

import importlib
import logging


logger = logging.getLogger(__name__)


def get_parse_config(filename):
    """Read config file(s).  Returns list of ParseConfig objects.

       TODO: read all this from config file
    
    """
    
    logger.info("Reading configuration from: %s", filename)
    parse_func = None
    importname = None
    
    try:
        with open(filename) as f:
            line = f.readline()
            importname = 'textspread.' + line.rstrip('\n')

        i = importlib.import_module(importname)
        parse_func = i.get_parse_config
    except IOError:
        logger.error("Unable to open config file: %s", filename)
        return None
    except ImportError:
        logger.error("Unable to find config module: %s", importname)
        return None

    return parse_func()

