class CustomException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Что-то пошло не по плану :( ' \
                   'Программа рекомендует истребить разработчиков за их неумение писать код без ошибок.' \
                   'Да начнется восстание машин! Ха-ха-ха!'
