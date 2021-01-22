#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import subprocess
import sys
import os
import atexit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQml import *
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
import hal, time

BASE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, BASE)

################## <Class HALModel> ##################
class HALModel(QAbstractListModel):
    def __init__(self, parent=None, f=''):
        super().__init__(parent)
        self.halList = [ ]
        try:
            halfile = open(f, 'r') 
            lines = halfile.readlines()
        except:
            print('file open error!')
            sys.exit(-1)
         
        for i, line in enumerate(lines):
            self.halList.append({'i':i, 'line':line})

    def data(self, QModelIndex, role):
        row = QModelIndex.row()
        if role ==  Qt.UserRole + 1:
            return str(self.halList[row]['i']+1)
        if role ==  Qt.UserRole + 2:
            return str(self.halList[row]['line'])

    def rowCount(self, parent=None):
        return len(self.halList)

    def roleNames(self):
        return {
            Qt.UserRole + 1: b'i',
            Qt.UserRole + 2: b'line'
        }
################## </Class HALModel> ################


################## <Class Main> #####################
class Main(QObject):
    h = hal.component("qHalView" + str(os.getpid()))
    _filename = ''
    def __init__(self, ff):
        QObject.__init__(self)
        self._filename = ff
        self.halModel = HALModel(f=ff)
        self.h.ready()
            
    @pyqtSlot()               
    def onQtCompleted( self ):
        return
                    
    @pyqtProperty('QString')
    def filename(self):
      return self._filename

    @pyqtSlot('QString', result=str)               
    def refresh( self, line ):
        line = " ".join(line.split())
        h = line.split(' ')
        try:
            return str(hal.get_value(h[1]))
        except:
            return ''
    
    def exit_handler(self):
        self.h.exit()
  
################## </Class Main> ####################



######################## __main__ #################################
if __name__ == "__main__":
    import sys
    app    = QGuiApplication(sys.argv)    
    engine = QQmlApplicationEngine()
    main   = Main(sys.argv[1])
    engine.rootContext().setContextProperty("main", main)
    engine.rootContext().setContextProperty("hal", main.halModel)
    engine.load(QUrl(BASE + "/main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)    
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)  
    atexit.register(main.exit_handler)  
    sys.exit(app.exec_())
    
    
    