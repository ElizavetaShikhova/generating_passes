import sys
from PyQt5.QtWidgets import QApplication
from front import MainWindow

app = QApplication(sys.argv)
ex = MainWindow()
ex.setStyleSheet(
    'background-image: url("src/background1.jpg");background-repeat: no-repeat; background-position: center;')
ex.setFixedSize(972, 600)
ex.show()
sys.exit(app.exec_())
