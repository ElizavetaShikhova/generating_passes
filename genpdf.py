from datetime import date
from typing import List
from person import Person, Status
from fpdf import FPDF, set_global


class GenPdf:
    def __init__(self):
        set_global('FPDF_CACHE_MODE', 1)  # отключение кэширования шрифтов (какую-то странную фичу добавили в этот ваш fpdf, нормальному человеку ничего кэшировать не надо)
        self.pdf = FPDF(unit='mm', format=(85.6, 53.98))  # создаем главный класс для работы с pdf, а также говорим, что будем использовать милиметры, и задаем размер для одной страницы
        self.pdf.add_font(family='PFM', style='normal', fname='src/pf.ttf', uni=True)  # добавляем
        self.pdf.add_font(family='PFM', style='bold', fname='src/pfm.ttf', uni=True)   # шрифты
        self.already_written = False
        # к сожалению этот прекрасый представитель программной фауны может "родить" pdf только один раз в жизни
        # чтобы еще раз напечатать pdf-ку надо заново инициализировать экземпляр

    # метод для более удобной смены цвета текста и его размера, аргументы и названия методов self.pdf интуитивно понятны
    def set_color_n_size(self, r, g, b, size):
        self.pdf.set_text_color(r, g, b)
        self.pdf.set_font_size(size)

    # данный метод генерирования шаблона пригождается для пропуска одному человеку и гостю/посетителю
    def __create_template(self):
        self.pdf.image('src/u.png', x=5, y=3, w=9.4, h=9, type='PNG')  # рисуем букву У

        # дальше все понятно, гы)
        self.pdf.set_font('PFM', 'bold')

        self.set_color_n_size(0, 0, 0, 11)
        self.pdf.text(20, 6, 'Уральский федеральный университет')

        self.set_color_n_size(0, 128, 0, 8.1)
        self.pdf.text(20, 10, 'СПЕЦИАЛИЗИРОВАННЫЙ УЧЕБНО-НАУЧНЫЙ ЦЕНТР')

    # метод для создания одной странички pdf одному человеку
    # если все плохо, то возвращает текст ошибки (а если все хорошо, то молчит)
    def create_person(self, person: Person) -> str:
        self.pdf.add_page()  # добавляем страничку

        self.__create_template()  # рисуем шаблончик

        # пишем фамилию и имя
        self.set_color_n_size(0, 0, 0, 16)
        self.pdf.text(32, 20, person.surname)
        self.pdf.text(32, 26, person.name)  # в оригинале отступ между строчками составляет 6мм, что сохранено в данной реализации

        # пишем статус человечка
        # в оригинале было так, что если статус == обучающийся, то это пишется на одной строке
        # иначе же первое слово ("Участник" или "Слушатель") пишется на первой строке
        # а остальное ("...мероприятия" или "...подготовительных курсов") на второй
        self.set_color_n_size(0, 0, 0, 10)
        if person.status == Status.student:  # простому работяге-ученику не нужны много строчек - хватит и одной
            self.pdf.text(32, 34, person.status.value)
        else:
            status_array = person.status.value.split(' ', 1)  # разделяем статус на первое слово и оставшиеся слова
            self.pdf.text(32, 34, status_array[0])  # пихаем
            self.pdf.text(32, 38, status_array[1])  # статус   (в оригинале отступ между строчками составляет 4мм, что сохранено в данной реализации)

        # если работяга-ученик живет не в Екб
        if person.dorm:
            self.pdf.image('src/hostel.png', 70, 30, 9.3, 8, type='PNG')  # то награждаем его за стремление к учебе и рисуем ему красивый красный домик, обозначающий общагу
            # - любите общагу!, - говорит один
            # - мать вашу!, - отвечают остальные
            # (общажный мем)

        self.pdf.set_font('PFM', 'normal')  # переключаемся на буквально "нормальный" шрифт
        self.set_color_n_size(0, 0, 0, 10)
        self.pdf.text(32, 45, f'Действительно по {person.expired.strftime("%d.%m.%Y")}')  # и пишем грустные слова о том, когда придется покидать наш любимый СУНЦ УрФУ

        try:
            self.pdf.image(person.photo, 5, 14, 24, 32, type='JPG')  # если все круто, то маленький художник, который сидит в FPDF.pdf.image, рисует главного героя этого пропуска
        except Exception as e:  # но всегда что-то может пойти не так, например, фото не доступно
            return f'Фотография для {person.name + " " + person.surname} не найдена'
            # волноваться не стоит - текст ошибки всегда один и тот же. он всегда говорит, что файлик не нашелся

        self.pdf.set_font('PFM', 'bold')  # пока вместо начального шрифта властвовал "нормальный", тот успел навестить бабушку в деревне и от этого потолстеть (ох уж эти бабушки, всегда тебя накормят, даже если ты только что сотню пирожков съел)
        self.set_color_n_size(0, 128, 0, 7)
        event_name = 'МЕРОПРИЯТИЯ' if person.status == Status.participant else 'ОБУЧЕНИЯ'  # название "мероприятия" в родительном падеже идет в переменную
        self.pdf.text(20, 51, f'ПО ОКОНЧАНИИ {event_name} ПОДЛЕЖИТ ВОЗВРАТУ')

        return ''  # а если все круто, то и текст ошибки возвращать не надо, какой же прекрасной иногда бывает жизнь

    # метод для генерации пропусков для всех, кто есть в списке
    # если все плохо, то возвращает текст ошибки (а если все хорошо, то молчит)
    def create_group(self, people: List[Person]) -> str:
        for person in people:
            alles_kaputt = self.create_person(person)  # alles kaputt (с нем. досл. "все сломано". - прим. ред.)
            if alles_kaputt:
                return alles_kaputt
        return ''

    # делаем пропуски для гостей/посетителей
    # удивительно, но даже тут могут быть ошибки, текст которых возвращается, если они есть
    def create_guests(self, start_number: int, total_number: int, ) -> str:
        # группа крови - на рукаве
        # мой порядковый номер- на рукаве...
        # (serial_number - порядковый номер. - прим. ред.)

        if start_number <= 0 or total_number <= 0:
            return 'Ты че, самый умный? А ну живо убрал ненатуральные числа!\n Are you kidding me? Remove non-natural numbers NOW!'

        for serial_number in range(start_number, start_number+total_number):
            self.pdf.add_page()  # добавляем новую страничку
            self.__create_template()  # рисуем шаблончик

            self.pdf.set_font('PFM', 'bold')
            self.set_color_n_size(0, 0, 0, 20)
            self.pdf.text(25, 25, 'ПОСЕТИТЕЛЬ')  # нет блин, гость

            self.pdf.set_font('PFM', 'normal')
            self.set_color_n_size(0, 0, 0, 16)
            self.pdf.text(35, 35, f'№ {str(serial_number).rjust(4, "0")}')  # с помощью магии делаем так, чтобы номер всегда был 4-значным

            self.pdf.set_font('PFM', 'bold')
            self.set_color_n_size(0, 128, 0, 9)
            self.pdf.text(5, 50, 'ПРИ ВЫХОДЕ ОПУСТИТЕ КАРТУ В ЩЕЛЬ КАРТОПРИЁМНИКА')  # но никакой же щели картоприемника нету на входе в сунец, что за несуразица?

        return ''  # вернули пустоту в знак того, что все ок

    # мы писали, мы писали - наши пальчики устали
    # (поэтому вместо тетрадки пишем в pdf)
    def write(self, output_file: str):
        if self.already_written:  # чтобы еще раз напечатать pdf-ку надо заново инициализировать экземпляр
            return
        self.pdf.output(output_file)
        self.already_written = True


# пример использования
'''

if __name__ == '__main__':
    generator = GenPdf()
    generator.create_person(Person('Эйнштейн', 'Альберт', Status.student, True, date(2023, 9, 1), 'src/test_photo.jpg'))
    generator.write('aboba.pdf')
    
    # в сотый раз повторяю, что для повторной генерации надо переинициализировать экземпляр класса
    generator.__init__()
    generator.create_guests(2, 13)
    generator.write('amogus.pdf')

#'''