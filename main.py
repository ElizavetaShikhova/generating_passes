import ctypes
import os

if os.name == 'nt':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Liza_plus_Sasha_inc')


def check_for_libs():
    try:
        import fpdf
        import PyQt5
    except ModuleNotFoundError:
        if os.name == 'nt':
            os.system('pip install fpdf pyqt5')


check_for_libs()
del check_for_libs


import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from front import MainWindow

app = QApplication(sys.argv)
icon = QIcon()
icon.addFile('src/icons/ico_halfsize.png', QSize(25, 19))
icon.addFile('src/icons/ico_x1.png', QSize(48, 36))
icon.addFile('src/icons/ico_x2.png', QSize(96, 72))
icon.addFile('src/icons/ico_x3.png', QSize(144, 108))
icon.addFile('src/icons/ico_x4.png', QSize(192, 144))
app.setWindowIcon(icon)
ex = MainWindow()
ex.setFixedSize(972, 600)
ex.show()
sys.exit(app.exec_())
