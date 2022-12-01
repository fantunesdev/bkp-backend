from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from backup.databases import database
from backup.entities.backup import Backup
from backup.queries import backup_query


class BackupRepository:
    def __init__(self, session: Session, *new_backup: Backup):
        """Construtor de BackupRepository."""
        self.__backup = new_backup
        self.session = session
        self.queries = backup_query.BackupQuery(self.session)

    @property
    def backup(self):
        return self.__backup

    @backup.setter
    def backup(self, backup):
        if isinstance(backup, Backup):
            self.__backup = backup
        else:
            self.__backup = Backup(
                description=backup.description,
                source=backup.source,
                target=backup.target,
                program=backup.program,
                options=backup.options,
                frequency=backup.frequency,
            )

    def create_backup(self, new_backup: Backup):
        self.__backup = new_backup
        if self.__backup.is_valid():
            new_db_backup = database.Backup(
                description=self.__backup.description,
                source=self.__backup.source,
                target=self.__backup.target,
                program=self.__backup.program,
                options=self.__backup.options,
                frequency=self.__backup.frequency,
            )
            self.queries.create_backup(new_db_backup)

    def get_backups(self):
        return self.queries.get_backups()

    def get_backup_by_id(self, bakcup_id: int):
        try:
            return self.queries.get_backup_by_id(bakcup_id)
        except NoResultFound:
            return None

    def get_backup_by_frequency(self, frequency_id: int):
        try:
            return self.queries.get_backup_by_frequency(frequency_id)
        except NoResultFound:
            return None

    def get_backup_by_description_and_frequency(self, backup):
        try:
            return self.queries.get_backup_by_description_and_frequency(backup)
        except NoResultFound:
            return None

    def delete_backup(self, backup: Backup):
        self.queries.delete_backup(backup)

    def delete_backup_by_id(self, backup_id: int):
        self.queries.delete_backup_by_id(backup_id)
