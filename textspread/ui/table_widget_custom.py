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
#  table_widget_custom.py
#
#  A QTableWidget that does copy and paste properly (or at least good enough).
#  
#  For details see:
#    http://www.voidynullness.net/blog/2013/06/21/qt-qtablewidget-copy-paste-row-into-excel/
#

import PySide.QtCore
import PySide.QtGui 


class TableWidgetCustom(PySide.QtGui.QTableWidget):
    def __init__(self, parent=None):
        super(TableWidgetCustom, self).__init__(parent)

    def keyPressEvent(self, event):
        if event.matches(PySide.QtGui.QKeySequence.Copy):
            self.copy()
        else:
            PySide.QtGui.QTableWidget.keyPressEvent(self, event)

    def copy(self):
        selection = self.selectionModel()
        indexes = selection.selectedRows()
        if len(indexes) < 1:
            #print "less than 1 index"
            return

        text = ''

        for idx in indexes:
            row = idx.row()
            #print row
            for col in range(0, self.columnCount()):
                item = self.item(row, col)
                if item:
                    text += item.text()
                text += '\t'
            text += '\n'

        PySide.QtGui.QApplication.clipboard().setText(text);

