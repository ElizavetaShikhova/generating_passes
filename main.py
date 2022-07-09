import sys
from PyQt5.QtWidgets import QApplication
from front import MainWindow

app = QApplication(sys.argv)
ex = MainWindow()
ex.setFixedSize(972, 600)
ex.show()
sys.exit(app.exec_())
