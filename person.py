from datetime import date
from enum import Enum
from exception import CustomException
from datetime import datetime


class Status(Enum):
    student = 'ОБУЧАЮЩИЙСЯ'
    participant = 'УЧАСТНИК МЕРОПРИЯТИЯ'
    prep_course_student = 'СЛУШАТЕЛЬ ПОДГОТОВИТЕЛЬНЫХ КУРСОВ'


class Person:
    def __init__(self, surname: str, name: str, expired: date, status: Status, dorm: bool, photo: str):
        self.surname = surname
        self.name = name
        self.expired = expired
        self.status = status
        self.dorm = dorm
        self.photo = photo

    def check(self):
        for i in [self.dorm, self.name, self.surname,
                  self.photo]:  # Проверяем, все ли переменные имеют значение !None
            if i is None:
                raise CustomException('Не хватает данных')

        if 'jpg' not in self.photo[-4:] and 'jpeg' not in self.photo[-4:]: # проверяем формат фото
            raise CustomException('Неверный формат фото')

        if self.expired <= datetime.now():  # не прошел ли срок окончания действия пропуска
            raise CustomException('Неверная дата')

