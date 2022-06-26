from datetime import date
from enum import Enum


class Status(Enum):
    student = 'ОБУЧАЮЩИЙСЯ'
    participant = 'УЧАСТНИК МЕРОПРИЯТИЯ'
    prep_course_student = 'СЛУШАТЕЛЬ ПОДГОТОВИТЕЛЬНЫХ КУРСОВ'


class Person:
    def __init__(self, surname: str, name: str, status: Status, dorm: bool, expired: date, photo: str):
        self.surname = surname
        self.name = name
        self.status = status
        self.dorm = dorm
        self.expired = expired
        self.photo = photo
