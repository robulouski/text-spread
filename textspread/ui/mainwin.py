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
#  mainwin.py
#
#
#  mainwin.py
#  Application's main window
#
import sys
from PySide.QtCore import *
from PySide.QtGui import *


from textspread import VERSION_STRING, APPLICATION_NAME
from textspread.ui.table_widget_custom import TableWidgetCustom 
from textspread.config import get_parse_list


class ResultTab(object):
    pass


class MainWindow(QMainWindow):
    def __init__(self, cfgfiles=None):
        super(MainWindow, self).__init__()
        self.resize(1130, 500)
        # Is this necessary???
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        status = self.statusBar()
        #status.setSizeGripEnabled(False)
        #status.addPermanentWidget(self.sizeLabel)
        status.showMessage(APPLICATION_NAME + ' ' + VERSION_STRING)    
        self.setWindowTitle(APPLICATION_NAME)       
        self.createMenus()
        self.tabWidget = QTabWidget()

        # 
        # Display results.  One tab for each file.  Each tab contains a 
        # (custom) QTableWidget.
        #        
        self.parseList = None
        self.configFilenames = cfgfiles
        self.loadData();
        self.populateData();
        self.setCentralWidget(self.tabWidget)

    def populateData(self):
        if not self.parseList:
            return

        #self.tabList = []
        for p in self.parseList:
            resultTable = TableWidgetCustom()
            #t = ResultTab()
            #t.parseConfig = p
            #t.resultTable = resultTable
            if p.column_list and len(p.column_list) > 0:
                resultTable.setColumnCount(len(p.column_list))
                resultTable.setHorizontalHeaderLabels(p.column_list)
                if p.result_list:
                    resultTable.setRowCount(len(p.result_list))
                    row_index = 0
                    for row in p.result_list:
                        for col in range(0, len(p.column_list)):
                            if row[col]:
                                item = QTableWidgetItem(row[col])
                                resultTable.setItem(row_index, col, item)
                        row_index = row_index + 1
                    if row_index > 0:
                        resultTable.setCurrentCell(row_index - 1, 0)
            self.tabWidget.addTab(resultTable, p.name)
            #self.tabList.append(t)
        

    def loadData(self):
        plist = get_parse_list(self.configFilenames)
        if not plist:
            logging.error("Oops!  Error loading data!")
            QMessageBox.warning(self, "Error", "Error loading data")
            #sys.exit("ERROR ABORT")
        self.parseList = plist

    def refreshData(self):
        self.tabWidget.clear()
        self.loadData()
        self.populateData();


    def createMenus(self):
        fileRefreshAct = QAction("Refresh", self, shortcut="F5",
                statusTip="Reload all data",
                triggered=self.refreshData)
        fileExitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)
        
        helpAboutAct = QAction("&About", self,
                statusTip="Show About box",
                triggered=self.about)
        
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(fileRefreshAct)
        self.fileMenu.addAction(fileExitAct)
        
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(helpAboutAct)
        
    def about(self):
        about_text = "<h1>" + APPLICATION_NAME + "</h1>" + \
           "Version " + VERSION_STRING + " " 
        about_text += """
<p>Design and coding by Robert Iwancz <br />
Copyright (c) 2013-2014</p>
<p><a href="http://www.voidynullness.net">www.voidynullness.net</a></p>
<center><p>___ </p></center>
<p>This application is free software released under the GNU General Public License.  It is distributed WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p>
"""
        QMessageBox.about(self, "About", about_text)
 
        
