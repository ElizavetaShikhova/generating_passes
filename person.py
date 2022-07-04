from datetime import date
from enum import Enum


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


