from datetime import datetime

from backup.databases import database
from backup.engines import server_mysql_engine
from backup.entities import relatory
from backup.repositories import frequency_repository, relatory_repository
from engines import local_psql_engine
from entities import backup
from repositories import os_repository, backup_repository

psql_engine = local_psql_engine.LocalPsqlEngineConnection()
local_psql_session = psql_engine.make_session()

mysql_engine = server_mysql_engine.ServerMysqlEngineConnection()
server_mysql_session = mysql_engine.make_session()

try:
    # database.create_tables(psql_engine)
    repository_backup = backup_repository.BackupRepository(local_psql_session)
    repository_frequency = frequency_repository.FrequencyRepository(local_psql_session)
    new_relatory = relatory.Relatory(
        backup=repository_backup.get_backup_by_id(1),
        status=True,
        frequency=repository_frequency.get_frequency_by_id(2),
        date=None,
        log='Isto é um teste.'
    )
    repository_relatory = relatory_repository.RelatoryRepository(local_psql_session)
    # repository_relatory.create_relatory(new_relatory)
    relatory = repository_relatory.get_relatory_by_id(2)
    print(relatory)
    print('novo teste')
    relatories = repository_relatory.get_relatories_by_date('2022-11-26')
    for relatory in relatories:
        print(relatory)

    # new_backup = backup.Backup(
    #     description='Pasta Teste',
    #     source='/home/fernando/teste',
    #     target='/home/fernando/teste-backup',
    #     need_compress=False,
    #     rsync_options='-uahv',
    # )
    # if new_backup.is_valid():
    #     repository_backup = backup_repository.BackupRepository(local_psql_session, new_backup)
    #     repository_backup.create_backup(new_backup)
    #     for backup in repository_backup.get_backups():
    #         print(backup)
    # repository_backup = backup_repository.BackupRepository(local_psql_session)
    # repository_backup.backup = repository_backup.get_backup_by_id(3)
    # repository_os = os_repository.OsRepository(repository_backup.backup)
    # repository_os.make_backup()

finally:
    local_psql_session.close()
    server_mysql_session.close()
