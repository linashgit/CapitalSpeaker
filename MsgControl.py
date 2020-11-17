from PyQt5.QtGui import QStandardItem
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt

class MsgControl:
    def __init__(self):
        return

    # 顯示各功能狀態用的function
    def writeMessage(self, msg, textEdit):
        textEdit.append(msg)

    def writeTableStocks(self, rownum, _list, model):
        for col in range(len(_list)):
            s = str(_list[col])
            model.setItem(rownum, col, QStandardItem(s))


class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

