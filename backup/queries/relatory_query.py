from sqlalchemy import func
from datetime import datetime

from backup.databases import database


class RelatoryQuery:
    def __init__(self, session):
        """Método construtor de RelatoryQuery."""
        self.session = session

    def create_relatory(self, relatory: database.Relatory):
        self.session.add(relatory)
        self.session.commit()

    def get_relatories(self):
        return self.session.query(database.Relatory)

    def get_relatory_by_id(self, relatory_id):
        return self.session.get(database.Relatory, relatory_id)

    def get_relatory_by_date(self, date):
        return self.session.query(database.Relatory).filter(
            func.DATE(database.Relatory.date) == date
        )

    def get_relatory_by_backup_and_date(self, backup: database.Backup, date):
        relatories_db = self.session.query(database.Relatory)\
            .filter(func.DATE(database.Relatory.date) == date)\
            .filter(backup.id == database.Relatory.backup)
        return relatories_db

    def remove_relatory(self, relatory):
        self.session.delete(relatory)
        self.session.commit()
