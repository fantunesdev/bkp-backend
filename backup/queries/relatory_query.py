from sqlalchemy import func

from backup.databases import database


class RelatoryQuery:
    def __init__(self, session):
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

    def remove_relatory(self, relatory):
        self.session.delete(relatory)
        self.session.commit()
