from datetime import datetime

from backup.databases import database
from backup.queries import relatory_query


class RelatoryRepository:
    def __init__(self, session):
        self.session = session
        self.__queries = relatory_query.RelatoryQuery(self.session)

    def create_relatory(self, relatory):
        new_relatory = database.Relatory(
            backup=relatory.backup.id,
            status=relatory.status,
            date=datetime.now(),
            log=relatory.log,
        )
        self.__queries.create_relatory(new_relatory)

    def get_relatories(self):
        return self.__queries.get_relatories()

    def get_relatory_by_id(self, relatory_id):
        return self.__queries.get_relatory_by_id(relatory_id)

    def get_relatories_by_date(self, date: datetime):
        if isinstance(date, datetime):
            date_str = date.strftime('%Y-%m-%d')
            return self.__queries.get_relatory_by_date(date_str)
        return self.__queries.get_relatory_by_date(date)
