# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        font16 = QtGui.QFont()
        font16.setPixelSize(16)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(972, 600)
        MainWindow.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(308, 20, 355, 47))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPixelSize(32)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(343, 100, 286, 32))
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.comboBox.setFont(font)
        self.comboBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setGeometry(QtCore.QRect(361, 150, 250, 31))
        self.lineEdit.setFont(font16)
        self.lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit.setAcceptDrops(True)
        self.lineEdit.setStyleSheet("border: 1px solid black")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(361, 190, 250, 31))
        self.lineEdit_2.setFont(font16)
        self.lineEdit_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_2.setStyleSheet("border: 1px solid black")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setClearButtonEnabled(False)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(361, 240, 250, 28))
        self.comboBox_2.setFont(font16)
        self.comboBox_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(373, 280, 226, 17))
        self.radioButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.radioButton.setFont(font16)
        self.radioButton.setObjectName("radioButton")

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(373, 310, 226, 17))
        self.radioButton_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.radioButton_2.setFont(font16)
        self.radioButton_2.setObjectName("radioButton_2")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(366, 350, 240, 51))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(351, 460, 271, 21))
        self.label_3.setObjectName("label_3")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(398, 420, 176, 31))
        self.pushButton_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        font = QtGui.QFont()
        font.setPixelSize(17)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background:rgb(49, 45, 32);color:rgb(255,255,255);")
        self.pushButton_2.setObjectName("pushButton")

        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(359, 500, 251, 22))
        self.dateEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        font = QtGui.QFont()
        font.setPixelSize(15)
        self.dateEdit.setFont(font)
        self.dateEdit.setObjectName("dateEdit")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(370, 540, 232, 41))
        self.pushButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        font = QtGui.QFont()
        font.setPixelSize(19)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background:rgb(49, 45, 32);color:rgb(255,255,255);")
        self.pushButton.setObjectName("pushButton")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(226, 157, 524, 261))
        self.label_4.setFont(font16)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(376, 150, 220, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPixelSize(18)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(435, 200, 102, 22))
        self.spinBox.setFont(font16)
        self.spinBox.setObjectName("spinBox")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(403, 240, 166, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPixelSize(18)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(435, 280, 102, 22))
        self.spinBox_2.setFont(font16)
        self.spinBox_2.setObjectName("spinBox_2")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(87, 30, 120, 50))
        font = QtGui.QFont()
        font.setPixelSize(26)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color:rgb(0, 255, 0)")
        self.label_7.setObjectName("label_7")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(390, 210, 192, 71))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background:rgb(49, 45, 32);color:rgb(255,255,255);")
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(390, 330, 192, 71))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("background:rgb(49, 45, 32);color:rgb(255,255,255);")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(390, 450, 192, 71))
        font = QtGui.QFont()
        font.setPixelSize(21)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("background:rgb(49, 45, 32);color:rgb(255,255,255);")
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(405, 480, 162, 31))
        font = QtGui.QFont()
        font.setPixelSize(17)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("background:rgb(49, 45, 32);color:rgb(255,255,255);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(875, 12, 90, 41))
        font = QtGui.QFont()
        font.setPixelSize(19)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("background:rgb(225, 206, 147)")
        self.pushButton_7.setObjectName("pushButton_7")

        pixmap = QtGui.QPixmap('src/checkbox.png')
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(590, 420, 31, 31))
        self.label_9.setPixmap(pixmap)
        font = QtGui.QFont()
        font.setPixelSize(17)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(590, 480, 31, 31))
        self.label_10.setPixmap(pixmap)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(340, 145, 292, 21))
        font = QtGui.QFont()
        font.setPixelSize(16)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")

        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(815,390, 92, 21))
        self.pushButton_8.setText('О программе)')
        self.pushButton_8.setStyleSheet('background:rgba(255,255,255,0);color:rgb(140,110,70);')
        font = QtGui.QFont()
        font.setPixelSize(14)
        font.setUnderline(True)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")

        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(243, 155, 524, 290))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPixelSize(14)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 972, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Генерирование пропусков"))
        self.label.setText(
            _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:27px;\">Генерирование\n"
                                     "                        пропусков</span></p></body></html>\n"
                                     "                    "))
        self.comboBox.setCurrentText(_translate("MainWindow", "Одному человеку"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Одному человеку"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Нескольким людям"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Посетителям"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Фамилия"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Имя"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Обучающийся"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Слушатель ПК"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Участник мероприятия"))
        self.radioButton.setText(_translate("MainWindow", "Проживает в общежитии"))
        self.radioButton_2.setText(_translate("MainWindow", "Не проживает в общежитии"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\"\n"
                                                      "                        font-size:15px;\">Выберите файл с фотографией</span></p><p align=\"center\"><span\n"
                                                      "                        style=\" font-size:15px;\">(jpg, 3:4, ширина не менее 300px)</span></p></body></html>\n"
                                                      "                    "))
        self.label_3.setText(
            _translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16px;\">Окончание\n"
                                     "                        срока действия пропуска</span></p></body></html>\n"
                                     "                    "))
        self.pushButton.setText(_translate("MainWindow", "Сгенерировать пропуск"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\"\n"
                                                      "                        font-size:15px; font-weight:100;\">Инфа о входных данных(будет позже)</span></p></body></html>\n"
                                                      "                    "))
        self.label_5.setText(_translate("MainWindow", "Количество пропусков"))
        self.label_6.setText(_translate("MainWindow", "Начальный номер"))
        self.label_11.setText(_translate("MainWindow", """
         Привет! Меня зовут Плюшка! Все пандочки любят играть
       в прятки. Я и Соня спрятались от Конфетки. Пока она нас
      ищет, я могу тебе рассказать о том, где мы обитаем.

   Мы находимся в программе, которая писалась с помощью любви
  и питона с 11 июня по 19 июля 2022 года. Ее делали
 замечательные ребята, которые не договорились, чье имя
 будет стоять впереди: Шихова Лиза и Сафронов Саша,
    которые закончат (или уже закончили) МатИнф
                   СУНЦа    УрФУ в 2023 году"""))
        self.pushButton_2.setText(_translate("MainWindow", "Выбрать фото"))
        self.label_7.setText(_translate("MainWindow", "Успешно"))
        self.pushButton_3.setText(_translate("MainWindow", "При помощи txt"))
        self.pushButton_4.setText(_translate("MainWindow", "При помощи csv"))
        self.pushButton_5.setText(_translate("MainWindow", "Таблицей внутри\nприложения"))
        self.pushButton_6.setText(_translate("MainWindow", "Выбрать файл"))
        self.pushButton_7.setText(_translate("MainWindow", "Назад ⇽"))
        self.label_8.setText(_translate("MainWindow", "Информация о входных данных"))
