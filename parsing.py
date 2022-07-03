from datetime import date, datetime
import os
import csv
from person import Person, Status
from PyQt5.QtWidgets import QTableWidget
from exception import CustomException


class Parser:
    def __init__(self):
        self.plist = []  # список с людьми

        # словарь(и) терминов (буквально)
        # наши придуманные форматы в txt/csv/таблице отличаются друг от друга, поэтому мне подумалось, что так будет удобнее

        # информацию о формате данных смотреть, не знаю, где ( на момент разработки она еще не опубликована:) )
        # возможно, в readme, но точно не тут
        self.__txt_terms = {
            'status_student': 'об',
            'status_participant': 'ум',
            'status_prep_course_student': 'пк',
            'dorm_yes': '',
            'dorm_no': 'общ'
        }
        self.__csv_terms = {
            'status_student': '',
            'status_participant': 'У',
            'status_prep_course_student': 'ПК',
            'dorm_yes': '',
            'dorm_no': 'общ'
        }
        self.__table_terms = {
            'status_student': 'об',
            'status_participant': 'ум',
            'status_prep_course_student': 'пк',
            'dorm_yes': 'д',
            'dorm_no': 'н'
        }
        self.terms = {'txt': self.__txt_terms, 'csv': self.__csv_terms, 'table': self.__table_terms}

    def clear(self):
        """
        чтоб поудобнее было очищать парсер в случае всяких нежданчиков
        """
        self.plist = []

    def __check_n_get_person(self, cur_terms: str, photos_dir: str, surname: str, name: str, expired: str, status: str, dorm: str) -> Person:
        """
        из названия понятно, что этот метод проверяет данные, и если они корректны, то возвращает объект Person
        cur_terms может быть одним из следующих значений: 'txt', 'csv', 'table'
        """

        # небольшая подготовка данных
        surname = surname.capitalize()
        name = name.capitalize()
        status = status.lower()
        dorm = dorm.lower()

        # создаем пустого, ничего из себя не представляющего человека для того
        # чтобы потом заполнить поля последовательно
        person = Person('', '', date(1, 1, 1), Status.student, False, '')

        if not surname:
            raise CustomException(f'Не введена фамилия для человека с именем "{name}"')
        if not name:
            raise CustomException(f'Не введено имя для человека с фамилией "{surname}"')

        person.surname = surname
        person.name = name

        _full_name_for_exceptions = person.surname + " " + person.name

        try:
            person.expired = datetime.strptime(expired, '%d.%m.%Y')
        except ValueError:
            self.clear()
            raise CustomException(f'Дата окончания срока действия пропуска для '
                            f'{_full_name_for_exceptions} введена неправильно: {expired}')

        if status == self.terms[cur_terms]['status_student']:
            person.status = Status.student
        elif status == self.terms[cur_terms]['status_participant']:
            person.status = Status.participant
        elif status == self.terms[cur_terms]['status_prep_course_student']:
            person.status = Status.prep_course_student
        else:
            self.clear()
            raise CustomException(f'Статус для {_full_name_for_exceptions} введен неправильно: {status}')

        if dorm == self.terms[cur_terms]['dorm_yes']:
            person.dorm = True
        elif dorm == self.terms[cur_terms]['dorm_no']:
            person.dorm = False
        else:
            self.clear()
            raise CustomException(f'Факт проживания в общежитии для {_full_name_for_exceptions} введен неправильно: {dorm}')

        _path_to_photo = photos_dir + os.sep + f'{person.surname}_{person.name}.jpg'
        if os.path.exists(_path_to_photo):
            person.photo = _path_to_photo
        else:
            self.clear()
            raise CustomException(f'Нет фотографии для {_full_name_for_exceptions}. Возможно, она есть, только подписана неправильно :)')

        return person

    def parse_from_txt(self, txt_fname: str, photos_dir: str):
        """
        парсим человечков из txt файла и добавляем в self.plist
        """
        with open(txt_fname, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                _surname, _name, _expired, _status, *_dorm = line.split()
                # т.к. формат подразумевает необязательный флаг - "общ", то приходится его через звездочку читать
                # поэтому _dorm является листом, который надо в str преобразовать путем взятия первого элемента
                # или понять, что там ничего нет и присвоить пустую строку
                _dorm = _dorm[0] if _dorm else ''
                person = self.__check_n_get_person('txt', photos_dir, _surname, _name, _expired, _status, _dorm)
                self.plist.append(person)

    def parse_from_csv(self, csv_fname: str, photos_dir: str):
        """
        парсим человечков из csv файла и добавляем в self.plist
        """
        with open(csv_fname, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for line in reader:
                _surname, _name, _status, _dorm, _expired = line
                person = self.__check_n_get_person('csv', photos_dir, _surname, _name, _expired, _status, _dorm)
                self.plist.append(person)

    def parse_from_table(self, table: QTableWidget, photos_dir: str):
        """
        парсим человечков из "фронтовой" таблицы и добавляем в self.plist
        """
        for cur_row_ind in range(table.rowCount()):
            _surname, _name, _expired, _status, _dorm = [table.item(cur_row_ind, i).text() for i in range(5)]
            if not (_surname or _name or _expired or _status or _dorm):
                continue
            person = self.__check_n_get_person('table', photos_dir, _surname, _name, _expired, _status, _dorm)
            self.plist.append(person)

    def get_person_list(self) -> list:
        return self.plist


# пример использования
'''

if __name__ == '__main__':
    parser = Parser()

    parser.parse_from_txt('samples/input_sample.txt', 'samples/')
    print('From txt:')
    print(*[[i.surname, i.name, i.expired.strftime('%d.%m.%Y'), i.status.value, i.dorm]
            for i in parser.get_person_list()], sep='\n')

    parser.clear()

    parser.parse_from_csv('samples/input_sample.csv', 'samples/')
    print('From csv:')
    print(*[[i.surname, i.name, i.expired.strftime('%d.%m.%Y'), i.status.value, i.dorm]
            for i in parser.get_person_list()], sep='\n')

#'''
