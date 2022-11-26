class BackupQuery:
    def create_backup(self, session, backup):
        session.add(backup)
        session.commit()
