import os
import sys

from backup.databases import database
from backup.engines import psql_engine
from backup.entities.backup import Backup
from backup.repositories import (
    backup_repository,
    frequency_repository,
    os_repository,
)

psql_engine = psql_engine.PsqlEngineConnection()
psql_session = psql_engine.make_session()

try:
    database.create_tables(psql_engine)
    repository_backup = backup_repository.BackupRepository(psql_session)
    repository_frequence = frequency_repository.FrequencyRepository(
        psql_session
    )
    try:
        param = sys.argv[1]
        backups_db = None
        if param in ('--sincronization', '-s'):
            backups_db = repository_backup.get_backup_by_frequency(1)
        elif param in ('-w', '--weekly'):
            backups_db = repository_backup.get_backup_by_frequency(3)
        else:
            raise IndexError

        if backups_db:
            for backup_db in backups_db:
                backup = Backup()
                new_backup = backup.convert(backup_db)
                repository_os = os_repository.OsRepository(new_backup)
                repository_os.make_backup(psql_session)
        else:
            raise IndexError
    except IndexError:
        print('Usage: backup [option]')
        print('-s, --sincronization     Backup de sincronização.')
        print('-w, --weekly             Backup semanal.')
        print('-m, --monthly            Backup mensal.')
finally:
    psql_session.close()
    os.system('vaultctl -s')
