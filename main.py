import sys
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox

from parsing import Parser
from genpdf import GenPdf
from person import Person, Status
from exception import CustomException


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/window.ui', self)
        self.hide_everything()
        self.comboBox.currentIndexChanged.connect(self.choose_mode)
        self.pushButton_2.clicked.connect(self.choose_photo)
        self.pushButton_6.clicked.connect(self.choose_file)
        self.pushButton.clicked.connect(self.make_pdf)
        self.pushButton_3.clicked.connect(self.from_txt)
        self.pushButton_4.clicked.connect(self.from_csv)
        self.pushButton_5.clicked.connect(self.from_exe)
        self.pushButton_7.clicked.connect(self.choose_mode)
        self.dateEdit.setDate(datetime.now())
        self.choose_mode()

        self.clear()
        '''self.dormitory - надо общагу или нет
        self.path_of_photo - строка с путем до фото
        self.path_of_dir - до папки с фото
        self.name - строка с именем
        self.surname - строка с фамилией
        self.date - строка(day.month.year) окончания срока действия
        self.path_of_pdf - куда сохранить pdf'''

    def pdf_for_one_person(self,generator):
        self.dormitory = self.radioButton.isChecked()
        self.surname = self.lineEdit.text().capitalize()
        self.name = self.lineEdit_2.text().capitalize()
        if self.comboBox_2.currentText() == 'Обучающийся':
            st = Status.student
        elif self.comboBox_2.currentText() == 'Слушатель ПК':
            st = Status.prep_course_student
        elif self.comboBox_2.currentText() == 'Участник мероприятия':
            st = Status.participant
        self.date = self.dateEdit.text()
        person = Person(self.surname, self.name, datetime.strptime(self.date, '%d.%m.%Y'), st, self.dormitory, self.path_of_photo)
        person.check()
        generator.create_person(person)

        generator.write(f'{self.path_of_pdf}/pdf_sample_1.pdf')

    def pdf_from_csv(self,generator,parser):
        if not self.path_of_file or not self.path_of_dir:
            raise CustomException('Не хватает данных')
        parser.parse_from_csv(self.path_of_file, self.path_of_dir)
        generator.create_group(parser.get_person_list())
        generator.write(f'{self.path_of_pdf}/pdf_sample_2.pdf')

    def pdf_for_visitors(self,generator):
        self.total_number = self.spinBox.value()  # кол-во пропусков
        self.start_number = self.spinBox_2.value()  # начальный номер
        generator.create_guests(self.start_number, self.total_number)
        generator.write(f'{self.path_of_pdf}/pdf_sample_3.pdf')

    def pdf_from_txt(self,generator,parser):
        if not self.path_of_file or not self.path_of_dir:
            raise CustomException('Не хватает данных')
        parser.parse_from_txt(self.path_of_file, self.path_of_dir)
        generator.create_group(parser.get_person_list())
        generator.write(f'{self.path_of_pdf}/propusk.pdf')

    def pdf_from_exe(self,generator,parser):
        if not self.path_of_dir:
            raise CustomException('Не хватает данных')
        parser.parse_from_table(self.table, self.path_of_dir)
        generator.create_group(parser.get_person_list())
        generator.write(f'{self.path_of_pdf}/pdf_sample_2.pdf')

    def make_pdf(self):
        self.path_of_pdf = QFileDialog.getExistingDirectory(self, "Выбрать папку, куда сохранить pdf", ".")
        try:
            generator = GenPdf()
            parser = Parser()
            if self.mode == 1:  # генерация пропуска для 1 человека
                self.pdf_for_one_person(generator)

            elif self.mode == 2:  # генерация пропусков для многих из csv
                self.pdf_from_csv(generator,parser)

            elif self.mode == 3:  # генерация пропусков для посетителей
                self.pdf_for_visitors(generator)

            elif self.mode == 4:  # для многих из txt
                self.pdf_from_txt(generator,parser)

            elif self.mode == 5:  # для многих из програмки
                self.pdf_from_exe(generator,parser)

        except Exception as er:
            if isinstance(er,CustomException): # Печатаем ошибку, если она кастомная
                self.show_error(str(er))
            else:
                self.show_error(str('Что-то пошло не так')) # иначе просто дружелюбно пишем
            print((str(er)))
            return

        self.clear()
        self.label_7.show()

    def show_error(self, text):
        self.label_7.hide()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("Error")
        msg.exec_()


    def choose_photo(self):  # сохраняем путь до фото
        if self.comboBox.currentText() == 'Нескольким людям':
            self.path_of_dir = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        else:
            self.path_of_photo = QFileDialog.getOpenFileName(self, 'Выбрать картинку(-и)', '')[0]


    def choose_file(self):
        self.path_of_file = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]


    def from_csv(self):
        self.hide_everything()
        self.mode = 2
        self.pushButton_2.setText('Выбрать папку c фото')
        self.pushButton_6.setText('Выбрать файл csv')
        self.show_widgets([self.pushButton_2, self.pushButton, self.label_4, self.pushButton_6,self.pushButton_7])


    def from_txt(self):
        self.hide_everything()
        self.mode = 4
        self.pushButton_2.setText('Выбрать папку c фото')
        self.pushButton_6.setText('Выбрать файл txt')
        self.show_widgets([self.pushButton_2, self.pushButton, self.label_4, self.pushButton_6,self.pushButton_7])


    def from_exe(self):
        self.hide_everything()
        self.mode = 5
        self.show_widgets([self.pushButton, self.pushButton_2,self.pushButton_7])

        self.pushButton_2.move(430, 480)

        self.table = QTableWidget(self)
        self.table.resize(561, 300)
        self.table.move(210, 165)
        self.table.setStyleSheet('background:rgb(255, 255, 255)')
        self.table.show()
        self.table.setColumnCount(5)
        self.table.setRowCount(100)
        for row in range(100):
            for col in range(5):
                self.table.setItem(row, col, QTableWidgetItem(''))

        a = ['Фамилия', 'Имя', 'Дата (д.м.г)', 'Статус (пк/ум/об)', 'Общежитие (д/н)']
        for i in range(len(a)):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(a[i]))


    def choose_mode(self):  # В зависимости от "режима" показываем определенные виджеты
        self.hide_everything()
        self.pushButton_2.move(430, 420)
        if self.comboBox.currentText() == 'Одному человеку':
            self.mode = 1
            self.pushButton_2.setText('Выбрать фото')
            self.show_widgets(
                [self.lineEdit, self.lineEdit_2, self.comboBox_2, self.radioButton, self.radioButton_2, self.label_2,
                 self.label_3, self.dateEdit, self.pushButton_2, self.pushButton])

        elif self.comboBox.currentText() == 'Нескольким людям':
            self.show_widgets([self.pushButton_3, self.pushButton_4, self.pushButton_5])

        elif self.comboBox.currentText() == 'Посетителям':
            self.mode = 3
            self.show_widgets([self.label_5, self.spinBox, self.label_6, self.spinBox_2, self.pushButton])


    def show_widgets(self, widgets):
        for i in widgets:
            i.show()


    def hide_everything(self):
        all_widgets = [self.dateEdit, self.spinBox, self.spinBox_2, self.radioButton, self.radioButton_2,
                       self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.dateEdit,
                       self.comboBox_2, self.lineEdit, self.lineEdit_2, self.pushButton_2, self.label_7,
                       self.pushButton_3, self.pushButton_4, self.pushButton_5, self.pushButton, self.pushButton_6,self.pushButton_7]
        for i in all_widgets:
            i.hide()
        try:
            self.table.hide()
        except Exception:
            pass


    def clear(self):
        self.dormitory, self.path_of_photo, self.name, self.surname, self.date, self.who, self.path_of_dir, self.path_of_pdf,self.path_of_file = None,None, None, None, None, None, None, None, None
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.dateEdit.setDate(datetime.now())

        try:
            self.table.clear()
            self.from_exe()
        except Exception:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.setStyleSheet(
        'background-image: url("src/background.jpg");background-repeat: no-repeat; background-position: center;')
    ex.setFixedSize(972, 690)
    ex.show()
    sys.exit(app.exec_())
