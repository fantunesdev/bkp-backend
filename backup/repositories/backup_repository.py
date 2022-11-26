import os.path

from sqlalchemy.orm.exc import NoResultFound, UnmappedInstanceError

from backup.databases import database
from backup.entities import backup


class BackupRepository:
    def create_backup(self, session, new_backup: backup.Backup):
        backup = database.Backup(
            description=new_backup.description,
            origin=new_backup.origin,
            target=new_backup.target,
            need_compress=new_backup.need_compress,
            rsync_options=new_backup.rsync_options,
        )
        session.add(backup)
        session.commit()

    def get_backups(self, session):
        return session.query(database.Backup)

    def get_bakcup_by_id(self, session, id: int):
        backup = session.get(database.Backup, id)
        if not backup:
            raise NoResultFound
        return backup

    def update_backup(self, session, new_backup: database.Backup):
        old_backup = self.get_bakcup_by_id(session, new_backup.id)
        old_backup.description = new_backup.description
        old_backup.origin = new_backup.origin
        old_backup.target = new_backup.target
        old_backup.need_compress = new_backup.need_compress
        old_backup.rsync_options = new_backup.rsync_options
        session.commit()

    def delete_backup(self, session, backup: backup.Backup):
        try:
            session.delete(backup)
            session.commit()
        except UnmappedInstanceError:
            print('Nenhum backup não encontrado.')

    def delete_backup_by_id(self, session, id: int):
        backup = self.get_bakcup_by_id(session, id)
        session.delete(backup)
        session.commit()
