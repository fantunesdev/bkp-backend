import os

from sqlalchemy.orm.session import Session

from backup.databases import database
from backup.entities.backup import Backup
from backup.queries import backup_query
from backup.repositories import os_repository


class BackupRepository:
    def __init__(self, session: Session, *new_backup: Backup):
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
                need_compress=backup.need_compress,
                rsync_options=backup.rsync_options,
            )

    def create_backup(self, new_backup: Backup):
        self.__backup = new_backup
        if self.__backup.is_valid():
            new_db_backup = database.Backup(
                description=self.__backup.description,
                source=self.__backup.source,
                target=self.__backup.target,
                need_compress=self.__backup.need_compress,
                rsync_options=self.__backup.rsync_options,
            )
            self.queries.create_backup(new_db_backup)

    def get_backups(self):
        return self.queries.get_backups()

    def get_backup_by_id(self, id: int):
        return self.queries.get_backup_by_id(id)

    def update_backup(self, new_backup: database.Backup):
        backup = Backup
        backup.description = new_backup.description
        backup.source = new_backup.source
        backup.target = new_backup.target
        backup.need_compress = new_backup.need_compress
        backup.rsync_options = new_backup.rsync_options

        if backup.is_valid():
            old_backup = self.get_backup_by_id(new_backup.id)
            old_backup.description = new_backup.description
            old_backup.source = new_backup.source
            old_backup.target = new_backup.target
            old_backup.need_compress = new_backup.need_compress
            old_backup.rsync_options = new_backup.rsync_options
            return self.queries.update_backup(new_backup)

    def delete_backup(self, backup: Backup):
        self.queries.delete_backup(backup)
        return None

    def delete_backup_by_id(self, backup_id: int):
        self.queries.delete_backup_by_id(backup_id)
