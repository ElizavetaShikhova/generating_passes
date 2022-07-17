from typing import List
from person import Person, Status
from fpdf import FPDF, set_global
from exception import CustomException


class GenPdf:
    def __init__(self):
        # отключение кэширования шрифтов (какую-то странную фичу добавили в этот ваш fpdf, нормальному человеку ничего кэшировать не надо)
        set_global('FPDF_CACHE_MODE', 1)
        # создаем главный класс для работы с pdf, а также говорим, что будем использовать милиметры, и задаем размер для одной страницы
        self.pdf = FPDF(unit='mm', format=(85.6, 53.98))
        # добавляем шрифты
        self.pdf.add_font(family='PFM', style='normal', fname='src/pf.ttf', uni=True)
        self.pdf.add_font(family='PFM', style='bold', fname='src/pfm.ttf', uni=True)
        # к сожалению этот прекрасый представитель программной фауны может "родить" pdf только один раз в жизни
        # чтобы еще раз напечатать pdf-ку надо заново инициализировать экземпляр
        self.already_written = False

    def set_color_n_size(self, r: int, g: int, b: int, size: int):
        """
        метод для более удобной смены цвета текста и его размера
        """
        self.pdf.set_text_color(r, g, b)
        self.pdf.set_font_size(size)

    def __create_template(self):
        """
        данный метод рисует шаблон, одинаковый для всех типов пропусков
        """
        self.pdf.image('src/u.png', x=5, y=3, w=9.4, h=9, type='PNG')  # рисуем букву У

        self.pdf.set_font('PFM', 'bold')

        self.set_color_n_size(0, 0, 0, 11)
        self.pdf.text(20, 6, 'Уральский федеральный университет')

        self.set_color_n_size(0, 128, 0, 8.1)
        self.pdf.text(20, 10, 'СПЕЦИАЛИЗИРОВАННЫЙ УЧЕБНО-НАУЧНЫЙ ЦЕНТР')

    def create_person(self, person: Person):
        """
        метод для создания одной странички pdf одному человеку
        """
        self.pdf.add_page()
        self.__create_template()

        # в оригинале отступ между строчками составляет 6мм, что сохранено в данной реализации
        self.set_color_n_size(0, 0, 0, 16)
        self.pdf.text(32, 20, person.surname)
        self.pdf.text(32, 26, person.name)

        # пишем статус человечка
        # в оригинале было так, что если статус == обучающийся, то это пишется на одной строке
        # иначе же первое слово ("Участник" или "Слушатель") пишется на первой строке
        # а остальное ("...мероприятия" или "...подготовительных курсов") на второй
        self.set_color_n_size(0, 0, 0, 10)
        if person.status == Status.student:  # простому работяге-ученику не нужны много строчек - хватит и одной
            self.pdf.text(32, 34, person.status.value)
        else:
            # разделяем статус на первое слово и оставшиеся слова
            # в оригинале отступ между строчками составляет 4мм, что сохранено в данной реализации
            status_array = person.status.value.split(' ', 1)
            self.pdf.text(32, 34, status_array[0])
            self.pdf.text(32, 38, status_array[1])

        # если работяга-ученик живет не в Екб
        if person.dorm:
            # то награждаем его за стремление к учебе и рисуем ему красивый красный домик, обозначающий общагу
            self.pdf.image('src/hostel.png', 70, 30, 9.3, 8, type='PNG')

        self.pdf.set_font('PFM', 'normal')
        self.set_color_n_size(0, 0, 0, 10)
        # пишем грустные слова о том, когда придется покидать наш любимый СУНЦ УрФУ
        self.pdf.text(32, 45, f'Действительно по {person.expired.strftime("%d.%m.%Y")}')

        self.pdf.rect(4.87, 13.87, 24.26, 32.26)  # это рамочка

        try:
            self.pdf.image(person.photo, 5, 14, 24, 32, type='JPG')
        except RuntimeError:
            raise CustomException(f'Фотография для {person.surname + " " + person.name} не найдена')

        self.pdf.set_font('PFM', 'bold')
        self.set_color_n_size(0, 128, 0, 7)
        # название "мероприятия" в родительном падеже идет в переменную
        event_name = 'МЕРОПРИЯТИЯ' if person.status == Status.participant else 'ОБУЧЕНИЯ'
        self.pdf.text(20, 51, f'ПО ОКОНЧАНИИ {event_name} ПОДЛЕЖИТ ВОЗВРАТУ')

    def create_group(self, people: List[Person]):
        """
        метод для генерации пропусков всем, кто есть в списке
        """
        for person in people:
            self.create_person(person)

    def create_guests(self, start_number: int, total_number: int):
        """
        делаем пропуски для гостей/посетителей
        """
        if start_number <= 0 or total_number <= 0:
            raise CustomException('Ты че, самый умный? А ну живо убрал ненатуральные числа!')

        for serial_number in range(start_number, start_number+total_number):
            self.pdf.add_page()
            self.__create_template()

            self.pdf.set_font('PFM', 'bold')
            self.set_color_n_size(0, 0, 0, 20)
            self.pdf.text(25, 25, 'ПОСЕТИТЕЛЬ')

            self.pdf.set_font('PFM', 'normal')
            self.set_color_n_size(0, 0, 0, 16)
            # с помощью магии делаем так, чтобы номер всегда был 4-значным
            self.pdf.text(35, 35, f'№ {str(serial_number).rjust(4, "0")}')

            self.pdf.set_font('PFM', 'bold')
            self.set_color_n_size(0, 128, 0, 9)
            # но никакой же щели картоприемника нету на входе в сунец, что за несуразица?
            self.pdf.text(5, 50, 'ПРИ ВЫХОДЕ ОПУСТИТЕ КАРТУ В ЩЕЛЬ КАРТОПРИЁМНИКА')

    def write(self, output_file: str):
        # чтобы еще раз напечатать pdf-ку надо заново инициализировать экземпляр
        if self.already_written:
            raise CustomException('Этот экземпляр класса уже однажды выписал пропуска (дайте ему отдохнуть, он устал). '
                                  'Чтобы еще раз написать pdf, надо переинициализировать его')
        self.pdf.output(output_file)
        self.already_written = True


# пример использования
'''

if __name__ == '__main__':
    from datetime import date
    from parsing import Parser

    generator = GenPdf()
    generator.create_person(Person('Эйнштейн', 'Альберт', date(2023, 9, 1), Status.student, True, 'samples/Эйнштейн_Альберт.jpg'))
    generator.write('samples/pdf_sample_1.pdf')

    generator.__init__()  # в сотый раз повторяю, что для повторной генерации надо переинициализировать экземпляр класса
    parser = Parser()
    parser.parse_from_txt('samples/input_sample.txt', 'samples/')
    generator.create_group(parser.get_person_list())
    generator.write('samples/pdf_sample_2.pdf')

    generator.__init__()
    generator.create_guests(2, 13)
    generator.write('samples/pdf_sample_3.pdf')

#'''
