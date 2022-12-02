class Relatory:
    def __init__(self, backup=None, status=None, date=None, log=None):
        """Método construtor."""
        self.backup = backup
        self.status = status
        self.date = date
        self.log = log

    def __eq__(self, other):
        """Verifica se dois objetos desta classe são iguais."""
        return self.backup == other.backup and self.status == other.status

    def __ne__(self, other):
        """Verifica se dois objetos desta classe são iguais."""
        return self.backup != other.backup and self.status != other.status
