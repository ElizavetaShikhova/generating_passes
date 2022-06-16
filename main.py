import sys
from datetime import datetime
from os import listdir
import csv

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('window.ui', self)
        self.hide_everything()
        self.comboBox.currentIndexChanged.connect(self.choose_mode)
        self.pushButton_2.clicked.connect(self.choose_photo)
        self.pushButton.clicked.connect(self.make_pdf)
        self.dateEdit.setDate(datetime.now())
        self.choose_mode()

        self.dormitory, self.path_of_photo, self.name, self.surname, self.date, self.who, self.path_of_dir = None, None, None, None, None, None, None
        '''self.dormitory - надо общагу или нет("общ"/"")
        self.path_of_photo - строка с путем до фото
        self.path_of_dir - до папки с scv и _photos
        self.name - строка с именем
        self.surname - строка с фамилией
        self.date - строка(!!!) окончания срока действия
        self.who - строка (""/ПК/У)'''

    def make_pdf(self):
        if self.ok():
            if self.mode == 1:  # генерация пропуска для 1 человека
                pass

            elif self.mode == 2:  # генерация пропусков для многих
                with open('C:/Users/User/Desktop/smth/sample.csv', encoding="utf8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                    for person in reader:
                        self.surname = person[0]
                        self.name = person[1]
                        self.who = person[2]
                        self.dormitory = person[3]
                        self.date = person[4]
                        self.path_of_photo = self.path_of_dir + f'/_photos/{self.surname}_{self.name}.jpg'
                        pass
                        #Все переменные приведены к тому же виду, что и для генерации для 1 человека, так что можно сделать отдельную одну функцию для этого

            else:  # генерация пропусков для посетителей
                self.count = self.spinBox.value() #кол-во пропусков(int)
                self.initial_number = self.spinBox_2.value() #начальный номер (int)


            self.dormitory, self.path_of_photo, self.name, self.surname, self.date, self.who,self.path_of_dir = None, None, None, None, None, None,None
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.dateEdit.setDate(datetime.now())
            '''Вроде обнулять надо тут, но это не точно :)
               Если ошибся в одном поле, нажал на кнопку, выпало исключение, человек исправил это одно поле, но обнулилось все,
                так что придется и фото заново прикреплять. Не очень удобно, поэтому обнулим после удачной генерации'''

    def ok(self):  # чекер
        self.label_7.hide()
        if self.mode == 1:
            if self.radioButton.isChecked():
                self.dormitory = 'общ'
            elif self.radioButton_2.isChecked():
                self.dormitory = ''
            if self.lineEdit.text() and self.lineEdit.text() != 'Фамилия':
                self.surname = self.lineEdit.text().capitalize()
            if self.lineEdit_2.text() and self.lineEdit_2.text() != 'Имя':
                self.name = self.lineEdit_2.text().capitalize()
            if self.comboBox_2.currentText() == 'Обучающийся':  # как бы оно выглядело в csv
                self.who = ""
            elif self.comboBox_2.currentText() == 'Слушатель ПК':
                self.who = "ПК"
            elif self.comboBox_2.currentText() == 'Участник мероприятия':
                self.who = "У"
            self.date = self.dateEdit.text()

            for i in [self.dormitory, self.name, self.surname,
                      self.path_of_photo]:  # Проверяем, все ли переменные имеют значение !None
                if i is None:
                    self.label_7.setText('Не хватает данных')
                    self.label_7.show()
                    return False
            if 'jpg' not in self.path_of_photo[-4:] and 'jpeg' not in self.path_of_photo[-4:]:  # вдруг, фото не jpg (но может и не надо такое)
                self.label_7.setText('Неверный формат\nфото')
                self.label_7.show()
                return False

            if datetime.strptime(self.date,
                                 '%d.%m.%Y') <= datetime.now():  # срок окончания действия пропуска уже прошел
                self.label_7.setText('Неверная дата')
                self.label_7.show()
                return False

        elif self.mode == 2:
            if not self.path_of_dir:
                self.label_7.setText('Не хватает данных')
                self.label_7.show()
                return False
            ldr = listdir(self.path_of_dir)
            if 'sample.csv' not in ldr or '_photos' not in ldr:  # проверяем, чтобы в папке были нужные файлы с нужными именами
                self.label_7.setText('В папке чего-то не\nхватает')
                self.label_7.show()
                return False
        return True

    def choose_photo(self):  # сохраняем путь до фото / до папки с scv и _photos
        if self.comboBox.currentText() == 'Нескольким людям':
            self.path_of_dir = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        else:
            self.path_of_photo = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

    def choose_mode(self):  # В зависимости от "режима" показываем определенные виджеты
        self.hide_everything()
        if self.comboBox.currentText() == 'Нескольким людям':
            self.mode = 2
            self.pushButton_2.setText('Выбрать папку')
            self.show_widgets([self.label_4, self.label_2, self.pushButton_2])

        elif self.comboBox.currentText() == 'Одному человеку':
            self.mode = 1
            self.pushButton_2.setText('Выбрать фото')
            self.show_widgets(
                [self.lineEdit, self.lineEdit_2, self.comboBox_2, self.radioButton, self.radioButton_2, self.label_2,
                 self.label_3, self.dateEdit, self.pushButton_2])
        elif self.comboBox.currentText() == 'Посетителям':
            self.mode = 3
            self.show_widgets([self.label_5, self.spinBox, self.label_6, self.spinBox_2])

    def show_widgets(self, widgets):
        for i in widgets:
            i.show()

    def hide_everything(self):
        all_widgets = [self.dateEdit, self.spinBox, self.spinBox_2, self.radioButton, self.radioButton_2,
                       self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.dateEdit,
                       self.comboBox_2, self.lineEdit, self.lineEdit_2, self.pushButton_2, self.label_7]
        for i in all_widgets:
            i.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.setStyleSheet(
        'background-image: url("background.jpg");background-repeat: no-repeat; background-position: center;')
    ex.setFixedSize(972, 690)
    ex.show()
    sys.exit(app.exec_())
