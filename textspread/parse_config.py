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
#  parse_config.py
#  
#  Primary parser module, implemented as possibly mis-named ParseConfig class.
#  Stores configuration data (input files) and parsing options (regexes).
#  Also does the actual parsing.
#


import re
import logging
import json

logger = logging.getLogger(__name__)



class ParseConfig(object):

    def __init__(self, name="undefined"):
        # 
        # Compulsory settings
        #
        self.name = name
        self.filepath = None
        self.column_list = None
        self.extract_list = []
        # Input file parsed in terms of "chunks", separated by markers, 
        # but which may (or may not) have header information in the first
        # line(s) of the chunk, that applies to everything in the chunk.
        # Chunks may contain one or more items/records.  If more than one,
        # it is separated within the chunk by a different (optional) 
        # marker.
        self.chunk_separator_re = None
        #
        # Optional Settings
        #
        self.main_regex = None
        self.item_separator_re = None #r'\s*--+\s*'
        # Chunks/items less than this length will not be parsed.
        self.item_min_length = 1
        self.is_header= False
        self.header_column_index = 0
        #
        # 
        #
        self.result_list = []


    def initialise(self, config):
        self.filepath = config.get("filename")
        logger.debug("Initialising ParseConfig: %s", self.name)
        if self.filepath:
            logger.debug("Using input file: %s", self.filepath)
        else:        
            logger.error("Missing filename in config")
            return True
        self.column_list = config["columns"]
        logger.debug("Columns: %d", len(self.column_list))
        self.chunk_separator_re = config["chunk-delimiter"]
        for ex in config["extract"]: 
            self.add_extract(ex["regex"], ex["mappings"], ex.get("subs", None))
        
        return False
    

    def add_extract(self, regex, mappings, subs=None):
        #print regex, mappings, subs
        self.extract_list.append((regex, mappings, subs))
        
    def parse(self):
        if not self.filepath:
            return
        
        f = open(self.filepath)
        logger.info("Parsing: %s", self.filepath)

        try:
            current_text = ""
            current_date = None
            for line in f:
                l = line.rstrip('\n')
                if re.match(self.chunk_separator_re, l):
                    if len(current_text) > self.item_min_length:
                        self.parse_main(current_date, current_text)
                    current_text = ""
                    current_date = None
                    continue
                if self.item_separator_re is not None and re.match(self.item_separator_re, l):
                    if len(current_text) > self.item_min_length:
                        self.parse_main(current_date, current_text)
                    current_text = ""
                    continue
                if current_date is None and re.search(r'\s*\d+/\d+/\d+\s*', l):
                    #print "Date: ", l
                    current_date = l
                    continue
                if len(current_text) > 0 and len(l) > 0:
                    current_text += " "
                current_text += l
            if len(current_text) > 10:
                self.parse_main(current_date, current_text)
        finally:
            f.close()

    def parse_main(self, block_date, block_text):
        #print "parsing: ", block_date
        is_main_match = False
        match_text = ""
        if self.main_regex is None:
            # Match everything if main regex is not specified
            is_main_match = True
            match_text = block_text
        else:
            m = re.search(self.main_regex, block_text, re.IGNORECASE)
            if m:
                #print "matched:"
                is_main_match = True
                match_text = m.group(1)
        if is_main_match:
            #print match_text
            #print '\n'
            self.parse_extract(block_date, match_text)
    
    def parse_extract(self, block_date, text):
        results = []
        for i in range(0, len(self.column_list)):
            results.append(None)
        if self.is_header:
            results[self.header_column_index] = block_date
        
        for ex in self.extract_list:
            regex = ex[0]
            maplist = ex[1]
            subs = ex[2]
            m = re.search(regex, text, re.IGNORECASE)
            if m:
                for ml in maplist:
                    res = m.group(ml[0])
                    if res:
                        r_index = ml[1]
                        if r_index >= len(self.column_list):
                            logger.error("MAPPING INDEX OUT OF BOUNDS: "
                                         "Skipping mapping to results index %d", 
                                         r_index)
                        else:
                            results[r_index] = res
            if subs:
                for s in subs:
                    res_index = s[0]
                    sub_list = s[1]
                    for sl in sub_list:
                        if results[res_index] and results[res_index].lower() == sl[0].lower():
                            results[res_index] = sl[1]
        self.result_list.append(results)
                    
