class Relatory:
    def __init__(self, backup=None, status=None, date=None, log=None):
        if backup:
            self.backup = backup
            self.status = status
            self.date = date
            self.log = log
