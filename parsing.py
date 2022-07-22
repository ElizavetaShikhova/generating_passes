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
        # наши придуманные форматы в txt/csv/таблице отличаются друг от друга, поэтому мне подумалось
        # что так будет удобнее

        # информацию о формате данных смотреть в readme.md
        __txt_n_csv_terms = {
            'status_student': '',
            'status_participant': 'ум',
            'status_prep_course_student': 'пк',
            'dorm_yes': 'общ',
            'dorm_no': ''
        }

        __table_terms = {
            'status_student': 'об',
            'status_participant': 'ум',
            'status_prep_course_student': 'пк',
            'dorm_yes': 'д',
            'dorm_no': 'н'
        }
        self.terms = {'txt': __txt_n_csv_terms, 'csv': __txt_n_csv_terms, 'table': __table_terms}

    def clear(self):
        """
        чтоб поудобнее было очищать парсер в случае всяких нежданчиков
        """
        self.plist = []

    def __check_n_get_person(self, cur_terms: str, photos_dir: str, surname: str, name: str, expired: str,
                             status: str, dorm: str) -> Person:
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
            raise CustomException(f'Пандочка не нашла фамилию для человека с именем "{name}"')
        if not name:
            raise CustomException(f'Пандочка не нашла имя для человека с фамилией "{surname}"')

        person.surname = surname
        person.name = name

        _full_name_for_exceptions = person.surname + " " + person.name

        try:
            person.expired = datetime.strptime(expired, '%d.%m.%Y')
        except ValueError:
            self.clear()
            raise CustomException(f'Пандочке не понравился формат даты окончания действия пропуска для {_full_name_for_exceptions}')

        if person.expired <= datetime.now():
            raise CustomException(f'Пандочке не понравился формат даты окончания действия пропуска для {_full_name_for_exceptions}')

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
            raise CustomException(f'Факт проживания в общежитии для {_full_name_for_exceptions} '
                                  f'введен неправильно: {dorm}')

        _path_to_photo = photos_dir + os.sep + f'{person.surname}_{person.name}.jpg'
        if os.path.exists(_path_to_photo):
            person.photo = _path_to_photo
        else:
            self.clear()
            raise CustomException(f'Нет фотографии для {_full_name_for_exceptions}. Возможно, она есть, '
                                  f'только подписана неправильно :)')

        return person

    def parse_from_txt(self, txt_fname: str, photos_dir: str):
        """
        парсим человечков из txt файла и добавляем в self.plist
        """

        if txt_fname[-3:] != 'txt':
            raise CustomException('Неверное расширение файла')

        with open(txt_fname, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if line == '':
                    continue
                try:
                    _surname, _name, _expired, *_flags = line.split()
                except ValueError:
                    raise CustomException('Слишком мало параметров для неизвестно кого, '
                                          'поэтому и неизвестно для кого слишком мало параметров')
                # формат подразумевает необязательные флаги для общаги и статуса, поэтому приходится их отдельно парсить
                # т.к. основная функция проверки не предусмотрена для этого
                if len(_flags) == 0:
                    _status = ''
                    _dorm = ''
                elif len(_flags) == 1:
                    if _flags[0] == self.terms['txt']['dorm_yes']:
                        _status = ''
                        _dorm = _flags[0]
                    else:
                        _status = _flags[0]
                        _dorm = ''
                elif len(_flags) == 2:
                    _status, _dorm = _flags
                else:
                    raise CustomException(f'Для {_surname + " " + _name} слишком много параметров')
                person = self.__check_n_get_person('txt', photos_dir, _surname, _name, _expired, _status, _dorm)
                self.plist.append(person)

    def parse_from_csv(self, csv_fname: str, photos_dir: str):
        """
        парсим человечков из csv файла и добавляем в self.plist
        """

        if csv_fname[-3:] != 'csv':
            raise CustomException('Неверное расширение файла')

        with open(csv_fname, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            line_counter = 0
            for line in reader:
                if len(line) == 0:
                    continue
                line_counter += 1
                if len(line) != 5:
                    raise CustomException(f'Неверное число параметров в {line_counter} строке')
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
