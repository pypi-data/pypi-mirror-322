#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from PySide6.QtWidgets import QApplication
import sys

try:
    import mainwindow as mw
except:
    import STEM_EDX.mainwindow as mw
    
def main():

    app = QApplication(sys.argv)

    # Get sccreen size to define app window geometry.
    (width, height) = app.screens()[0].size().toTuple()

    window = mw.Window()
    window.setFixedSize(width * 0.9, height * 0.9)
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()