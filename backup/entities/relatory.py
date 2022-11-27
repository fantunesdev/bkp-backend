class Relatory:
    def __init__(self, backup, status, frequency, date, log):
        self.__backup = backup
        self.__status = status
        self.__frequency = frequency
        self.__date = date
        self.__log = log

    @property
    def backup(self):
        return self.__backup

    @property
    def status(self):
        return self.__status

    @property
    def frequency(self):
        return self.__frequency

    @property
    def date(self):
        return self.__date

    @property
    def log(self):
        return self.__log
