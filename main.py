# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 10:27:59 2020

@author: li.nash
"""

import sys
from PyQt5.QtWidgets import QApplication
from mainModel import MainFrame

if __name__ == '__main__':
    print('start')
    app = QApplication(sys.argv)
    mainFrame  = MainFrame()
    mainFrame.show()
    sys.exit(app.exec_())

