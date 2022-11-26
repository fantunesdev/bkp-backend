import os

from sqlalchemy.orm.session import Session

from backup.databases import database
from backup.entities.backup import Backup
from backup.queries import backup_query
from backup.repositories import os_repository


class BackupRepository:
    def __init__(self, session: Session, new_backup: Backup):
        self.backup = new_backup
        self.session = session
        self.os_repository = os_repository.OsRepository(self.backup)
        self.queries = backup_query.BackupQuery(self.session)

    def create_backup(self, new_backup: Backup):
        self.backup = new_backup
        new_db_backup = database.Backup(
            description=self.backup.description,
            source=self.backup.source,
            target=self.backup.target,
            need_compress=self.backup.need_compress,
            rsync_options=self.backup.rsync_options,
        )
        self.queries.create_backup(new_db_backup)

    def get_backups(self):
        return self.queries.get_backups()

    def get_backup_by_id(self, id: int):
        return self.queries.get_backup_by_id(id)

    def update_backup(self, new_backup: database.Backup):
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
