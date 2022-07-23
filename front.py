from datetime import datetime

from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView

from parsing import Parser
from genpdf import GenPdf
from person import Person, Status
from exception import CustomException
from src.window import Ui_MainWindow


class MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.hide_everything()
        self.comboBox.currentIndexChanged.connect(self.choose_mode)
        self.pushButton_2.clicked.connect(self.choose_photo)
        self.pushButton_6.clicked.connect(self.choose_file)
        self.pushButton.clicked.connect(self.make_pdf)
        self.pushButton_3.clicked.connect(self.from_txt)
        self.pushButton_4.clicked.connect(self.from_csv)
        self.pushButton_5.clicked.connect(self.from_exe)
        self.pushButton_7.clicked.connect(self.choose_mode)
        self.pushButton_8.clicked.connect(self.about_prog)
        self.pushButton_9.clicked.connect(self.settings)
        self.dateEdit.setDate(datetime.now())
        self.choose_mode()

        self.clear()
        '''self.dormitory - надо общагу или нет
        self.path_of_photo - строка с путем до фото
        self.path_of_dir - строка с путем до папки с фото
        self.path_of_file = строка с путем до txt/csv
        self.name - строка с именем
        self.surname - строка с фамилией
        self.date - дата окончания срока действия
        self.path_of_pdf - куда сохранить pdf'''

    def check(self):
        """
        Проверка на корректность введенных данных для 1 человека
        """

        for i in [self.dormitory, self.name, self.surname,
                  self.path_of_photo]:  # Проверяем, все ли переменные имеют значение !None
            if i is None or i == '':
                raise CustomException('Пандочке не хватает данных')

        if 'jpg' not in self.path_of_photo[-4:] and 'jpeg' not in self.path_of_photo[-4:]:  # проверяем формат фото
            self.label_9.hide()
            raise CustomException('Пандочка ждёт другой формат фото')

        if self.date <= datetime.now():  # не прошел ли срок окончания действия пропуска
            raise CustomException('Пандочка думает,что это неверная дата')

    def preparing(self):
        self.dormitory = self.radioButton.isChecked()
        self.surname = self.lineEdit.text().capitalize()
        self.name = self.lineEdit_2.text().capitalize()
        self.date = datetime.strptime(self.dateEdit.text(), '%d.%m.%Y')
        if self.comboBox_2.currentText() == 'Обучающийся':
            self.st = Status.student
        elif self.comboBox_2.currentText() == 'Слушатель ПК':
            self.st = Status.prep_course_student
        elif self.comboBox_2.currentText() == 'Участник мероприятия':
            self.st = Status.participant

    def pdf_for_one_person(self, generator):
        """
        Генерация pdf для 1 человека
        """
        self.preparing()
        self.check()
        generator.create_person(Person(self.surname, self.name, self.date, self.st, self.dormitory, self.path_of_photo))
        self.path_of_pdf = self.choose_save_path()
        if self.path_of_pdf:
            generator.write(self.path_of_pdf)

    def pdf_from_csv(self, generator, parser):
        """
        Генерация pdf из csv
        """
        if not self.path_of_file or not self.path_of_dir:
            raise CustomException('Пандочке не хватает данных')
        parser.parse_from_csv(self.path_of_file, self.path_of_dir)
        generator.create_group(parser.get_person_list())
        self.path_of_pdf = self.choose_save_path()
        if self.path_of_pdf:
            generator.write(self.path_of_pdf)

    def pdf_for_visitors(self, generator):
        """
        Генерация пропусков для посетителей
        """
        self.total_number = self.spinBox.value()  # кол-во пропусков
        self.start_number = self.spinBox_2.value()  # начальный номер
        generator.create_guests(self.start_number, self.total_number)
        self.path_of_pdf = self.choose_save_path()
        if self.path_of_pdf:
            generator.write(self.path_of_pdf)

    def pdf_from_txt(self, generator, parser):
        """
        Генерация pdf из txt
        """
        if not self.path_of_file or not self.path_of_dir:
            raise CustomException('Пандочке не хватает данных')
        parser.parse_from_txt(self.path_of_file, self.path_of_dir)
        generator.create_group(parser.get_person_list())
        self.path_of_pdf = self.choose_save_path()
        if self.path_of_pdf:
            generator.write(self.path_of_pdf)

    def pdf_from_exe(self, generator, parser):
        """
        Генерация pdf из таблички
        """
        if not self.path_of_dir:
            raise CustomException('Пандочке не хватает данных')
        parser.parse_from_table(self.table, self.path_of_dir)
        generator.create_group(parser.get_person_list())
        self.path_of_pdf = self.choose_save_path()
        if self.path_of_pdf:
            generator.write(self.path_of_pdf)

    def choose_save_path(self):
        if self.radioButton_5.isChecked():
            return QFileDialog.getSaveFileName(self, self.tr("Сохранить файл"), f"/propusk", self.tr("PDF files (*.pdf)"),
                                            options=QFileDialog.DontUseNativeDialog)[0]
        return QFileDialog.getSaveFileName(self, self.tr("Сохранить файл"), f"/propusk",
                                           self.tr("PDF files (*.pdf)"))[0]

    def make_pdf(self):
        """
        Функция для кнопки генерации пропусков
        """
        try:
            generator = GenPdf()
            parser = Parser()

            if self.mode == 1:  # генерация пропуска для 1 человека
                self.pdf_for_one_person(generator)

            elif self.mode == 2:  # генерация пропусков для многих из csv
                self.pdf_from_csv(generator, parser)

            elif self.mode == 3:  # генерация пропусков для посетителей
                self.pdf_for_visitors(generator)

            elif self.mode == 4:  # для многих из txt
                self.pdf_from_txt(generator, parser)

            elif self.mode == 5:  # для многих из таблицы
                self.pdf_from_exe(generator, parser)

            if self.path_of_pdf:
                self.clear()
                self.label_7.show()  # Скажем, что все получилось

        except Exception as er:
            if self.mode != 1:
                self.label_9.hide()
                self.label_10.hide()
            if isinstance(er, CustomException):  # Печатаем ошибку, если она кастомная
                self.show_error(str(er))
            else:
                self.show_error(str(CustomException()))  # иначе просто дружелюбно пишем :)

    def show_error(self, text):
        """
        Окошко с ошибками
        """
        self.label_7.hide()
        if not self.path_of_file:
            self.label_10.hide()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("Error")
        msg.exec_()

    def choose_photo(self):
        if self.comboBox.currentText() == 'Нескольким людям':
            if self.radioButton_4.isChecked() or self.radioButton_5.isChecked():
                self.path_of_dir = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".",
                                                                    QFileDialog.DontUseNativeDialog)
            else:
                self.path_of_dir = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")

        else:
            if self.radioButton_5.isChecked():
                self.path_of_photo = \
                QFileDialog.getOpenFileName(self, 'Выбрать картинку(-и)', '', options=QFileDialog.DontUseNativeDialog)[
                    0]
            else:
                self.path_of_photo = QFileDialog.getOpenFileName(self, 'Выбрать картинку(-и)', '')[0]
        if self.path_of_photo or self.path_of_dir:
            self.label_9.show()

    def choose_file(self):
        if self.radioButton_5.isChecked():
            self.path_of_file = \
            QFileDialog.getOpenFileName(self, 'Выбрать файл', '', options=QFileDialog.DontUseNativeDialog)[0]
        else:
            self.path_of_file = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        if self.path_of_file:
            self.label_10.show()

    def from_csv(self):
        """
        Просто функция для показа виджетов для csv-режима
        """
        self.hide_everything()
        self.mode = 2
        self.pushButton_2.move(398, 420)
        self.label_9.move(590, 420)
        self.pushButton_2.setText('Выбрать папку c фото')
        self.pushButton_6.setText('Выбрать файл csv')
        self.label_4.setText("""
1. Фамилия
2. Имя
3. Статус: пустое (то есть две ; подряд) поле для обучающего,
"ПК" для слушателя подготовительных курсов,
"У" для участника мероприятия, тоже большими буквами
4. Факт проживания в общежитии. Пустое поле (то есть две ; подряд),
если человек не будет там проживать, общ если будет
5. Дата окончания действия пропуска в формате дд.мм.гггг

Название каждой фотографии, которая лежит в этой папке, должно
соответствовать формату Фамилия_Имя.jpg""")
        self.show_widgets(
            [self.pushButton_2, self.pushButton, self.label_4, self.pushButton_6, self.pushButton_7, self.label_8,
             self.pushButton_8, self.comboBox])

    def from_txt(self):
        """
        Просто функция для показа виджетов для txt-режима
        """
        self.hide_everything()
        self.mode = 4
        self.pushButton_2.move(398, 420)
        self.label_9.move(590, 420)
        self.pushButton_2.setText('Выбрать папку c фото')
        self.pushButton_6.setText('Выбрать файл txt')
        self.label_4.setText("""
1. Фамилия
2. Имя
3. Дата окончания действия пропуска в формате дд.мм.гггг
4. Статус: ничего не вписывайте для обучающегося, "ум" для участ-
 ника мероприятия, "пк" для слушателя подготовительных курсов. 
5. Если человечек будет жить в общежитии, то "общ",
 в ином случае ничего не пишите

Все параметры пишите через пробел и без кавычек,
а каждого человека описывайте в отдельной строке.
Название каждой фотографии, которая лежит в этой папке,
должно соответствовать формату Фамилия_Имя.jpg""")
        self.show_widgets(
            [self.pushButton_2, self.pushButton, self.label_4, self.pushButton_6, self.pushButton_7, self.label_8,
             self.pushButton_8, self.comboBox])

    def from_exe(self):
        """
        Просто функция для показа виджетов для режима таблицы
        """
        self.hide_everything()
        self.mode = 5
        self.show_widgets([self.pushButton, self.pushButton_2, self.pushButton_7, self.comboBox])
        self.set_background('src/background2.jpeg')

        self.table = QTableWidget(self)
        self.table.resize(636, 300)
        self.table.move(168, 160)

        self.table.setStyleSheet('background:rgb(255, 255, 255)')
        self.table.show()
        self.table.setColumnCount(5)
        self.table.setRowCount(100)

        self.pushButton_2.move(398, 480)
        self.label_9.move(590, 480)
        for row in range(100):
            for col in range(5):
                self.table.setItem(row, col, QTableWidgetItem(''))

        columns = ['Фамилия', 'Имя', 'Дата (дд.мм.гггг)', 'Статус (пк/ум/об)', 'Общежитие (д/н)']
        header = self.table.horizontalHeader()
        for i in range(len(columns)):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(columns[i]))
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def choose_mode(self):
        """
        Функция для выбора режима
        """
        self.hide_everything()
        self.set_background('src/background1.jpg')
        if self.comboBox.currentText() == 'Одному человеку':
            self.mode = 1
            self.pushButton_2.move(398, 420)
            self.label_9.move(590, 420)
            self.pushButton_2.setText('Выбрать фото')
            self.show_widgets(
                [self.lineEdit, self.lineEdit_2, self.comboBox_2, self.radioButton, self.radioButton_2, self.label_2,
                 self.label_3, self.dateEdit, self.pushButton_2, self.pushButton, self.pushButton_8, self.comboBox])

        elif self.comboBox.currentText() == 'Нескольким людям':
            self.show_widgets(
                [self.pushButton_3, self.pushButton_4, self.pushButton_5, self.pushButton_8, self.comboBox,
                 self.pushButton_9])

        elif self.comboBox.currentText() == 'Посетителям':
            self.mode = 3
            self.show_widgets(
                [self.label_5, self.spinBox, self.label_6, self.spinBox_2, self.pushButton, self.pushButton_8,
                 self.comboBox])

    def show_widgets(self, widgets):
        for i in widgets:
            i.show()

    def hide_everything(self):
        all_widgets = [self.dateEdit, self.spinBox, self.spinBox_2, self.radioButton, self.radioButton_2,
                       self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.dateEdit,
                       self.comboBox_2, self.lineEdit, self.lineEdit_2, self.pushButton_2, self.label_7,
                       self.pushButton_3, self.pushButton_4, self.pushButton_5, self.pushButton, self.pushButton_6,
                       self.pushButton_7, self.label_8, self.label_9, self.label_10, self.label_11, self.pushButton_8,
                       self.pushButton_9, self.radioButton_3, self.radioButton_4, self.label_12, self.radioButton_5]
        for i in all_widgets:
            i.hide()
        try:
            self.table.hide()
        except Exception:
            pass

    def clear(self):
        self.dormitory, self.path_of_photo, self.name, self.surname, self.date, self.who, self.path_of_dir, self.path_of_pdf, self.path_of_file = None, None, None, None, None, None, None, None, None
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.dateEdit.setDate(datetime.now())
        self.pushButton_2.move(398, 420)
        self.label_9.move(590, 420)
        self.label_9.hide()
        self.label_10.hide()
        try:
            self.table.clear()
        except Exception:
            pass
        if self.mode == 5:
            self.from_exe()

    def set_background(self, url):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(url)))
        self.setPalette(palette)

    def about_prog(self):
        self.hide_everything()
        self.comboBox.hide()
        self.show_widgets([self.label_11, self.pushButton_7])
        self.set_background('src/background3.jpg')

    def settings(self):
        self.hide_everything()
        self.comboBox.hide()
        self.show_widgets([self.pushButton_7, self.radioButton_3, self.radioButton_4, self.label_12, self.radioButton_5,
                           self.pushButton_8])
