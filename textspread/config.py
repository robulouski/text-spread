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

#import importlib
import logging
import json
import yaml
#from pprint import pprint

from textspread.parse_config import ParseConfig


logger = logging.getLogger(__name__)


def get_parse_config(filename):
    """Read config file(s).  Returns list of ParseConfig objects.

       TODO: read all this from config file
    
    """
    
    logger.info("Reading configuration from: %s", filename)
    config = None
    plist = []
    
    try:
        with open(filename) as f:
#            config = json.load(f)
            config = yaml.load(f)
    except IOError:
        logger.error("Unable to open config file: %s", filename)
        return None

    #if config:
    #    pprint(config)

    name = config.get("name")
    if not name:
        logger.error("Missing name in config: %s", filename)
        return None
    
    logger.debug("Creating ParseConfig: %s", name)
    pc = ParseConfig(name)
    pc.initialise(config)
    pc.parse()
    plist.append(pc)
    
    return plist

