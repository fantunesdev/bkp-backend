from sqlalchemy.orm.exc import NoResultFound, UnmappedInstanceError
from sqlalchemy.orm.session import Session

from backup.databases import database


class BackupQuery:
    def __init__(self, session: Session):
        self.session = session

    def create_backup(self, new_backup: database.Backup):
        self.session.add(new_backup)
        self.session.commit()

    def get_backups(self):
        return self.session.query(database.Backup)

    def get_backup_by_id(self, backup_id: int):
        db_backup = self.session.get(database.Backup, backup_id)
        if not db_backup:
            raise NoResultFound
        return db_backup

    def update_backup(self, new_backup: database.Backup):
        self.session.commit()

    def delete_backup(self, backup):
        self.session.delete(backup)
        self.session.commit()

    def delete_backup_by_id(self, backup_id: int):
        backup = self.get_backup_by_id(backup_id)
        self.session.delete(backup)
        self.session.commit()
