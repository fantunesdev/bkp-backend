from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from backup.databases import database


class BackupQuery:
    def __init__(self, session: Session):
        """A classe BackupQuery faz as queries do SQL-Alchemy para a classe Backup."""
        self.session = session

    def create_backup(self, new_backup: database.Backup):
        self.session.add(new_backup)
        self.session.commit()

    def get_backups(self):
        return self.session.query(database.Backup)

    def get_backup_by_id(self, backup_id: int):
        backup_db = self.session.get(database.Backup, backup_id)
        if not backup_db:
            raise NoResultFound
        return backup_db

    def get_backup_by_frequency(self, frequency_id: int):
        backups_db = self.session.query(database.Backup).filter(database.Backup.frequency == frequency_id)
        if not backups_db:
            raise NoResultFound
        return backups_db

    def get_backup_by_description_and_frequency(self, backup):
        backup_db = (
            self.session.query(database.Backup)
            .filter(
                database.Backup.description == backup.description
                and database.Backup.frequency == backup.frequency
            )
            .first()
        )
        if not backup_db:
            raise NoResultFound
        return backup_db

    def delete_backup(self, backup):
        self.session.delete(backup)
        self.session.commit()

    def delete_backup_by_id(self, backup_id: int):
        backup = self.get_backup_by_id(backup_id)
        self.session.delete(backup)
        self.session.commit()
