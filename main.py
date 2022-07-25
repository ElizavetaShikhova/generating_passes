import ctypes
import os

if os.name == 'nt':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Liza_plus_Sasha_inc')


import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'src', 'dependencies'))


from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from front import MainWindow

app = QApplication(sys.argv)
icon = QIcon()
icon.addFile('src/icons/ico_halfsize.ico', QSize(25, 19))
icon.addFile('src/icons/ico_x1.ico', QSize(48, 36))
icon.addFile('src/icons/ico_x2.ico', QSize(96, 72))
icon.addFile('src/icons/ico_x3.ico', QSize(144, 108))
icon.addFile('src/icons/ico_x4.ico', QSize(192, 144))
app.setWindowIcon(icon)
ex = MainWindow()
ex.setFixedSize(972, 600)
ex.show()
sys.exit(app.exec_())
