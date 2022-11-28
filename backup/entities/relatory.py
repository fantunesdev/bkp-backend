class Relatory:
    def __init__(self, backup, status, date, log):
        self.__backup = backup
        self.__status = status
        self.__date = date
        self.__log = log

    @property
    def backup(self):
        return self.__backup

    @property
    def status(self):
        return self.__status

    @property
    def date(self):
        return self.__date

    @property
    def log(self):
        return self.__log
