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
import sys
import logging
import json
import yaml

from textspread.parse_config import ParseConfig, ParseConfigError


logger = logging.getLogger(__name__)


def get_parse_config(filename):
    """Read a config file, create ParseConfig object from it.

    
    """
    
    logger.info("Reading configuration from: %s", filename)
    config = None
    
    with open(filename) as f:
        if filename.endswith(".json"):
            config = json.load(f)
        else:
            config = yaml.load(f)

#     if config:
#        from pprint import pprint
#        pprint(config)

    name = config.get("name")
    if not name:
        logger.error("Missing name in config: %s", filename)
        return None
    
    logger.debug("Creating ParseConfig: %s", name)
    pc = ParseConfig(name, config)

    return pc


def get_parse_list(filenames):
    """Returns list of ParseConfig objects, with parsed data.
    
    """
    
    config = None
    # This will be a list of ParseConfig object, returned at the end if successful.
    plist = []   

    logger.debug("READING CONFIG...")
        
    try:
        for f in filenames:
            p = get_parse_config(f)
            if not p:
                # Something went wrong, abort the whole thing
                return None
            plist.append(p)
    
        if len(plist) > 0:
            logger.debug("PARSING...")    
        else:
            logger.debug("Nothing to parse...finishing up.")
            return None 
        
        for p in plist:
            p.parse()
    
    except ParseConfigError as e:
        logger.error("Parse config error: %s", e.msg)
        return None
    except IOError as e:
        logger.error("File error %d: %s", e.errno, e.strerror)
        return None
    
    return plist    

    