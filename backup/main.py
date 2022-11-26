import subprocess

from backup.databases import database
from backup.engines import server_mysql_engine
from engines import local_psql_engine
from entities import backup
from repositories import os_repository, backup_repository

psql_engine = local_psql_engine.LocalPsqlEngineConnection()
local_psql_session = psql_engine.make_session()

mysql_engine = server_mysql_engine.ServerMysqlEngineConnection()
server_mysql_session = mysql_engine.make_session()

try:
    database.create_tables(psql_engine)
    new_backup = backup.Backup(
        description='Pasta Teste',
        source='/home/fernando/teste',
        target='/home/fernando/teste-backup',
        need_compress=False,
        rsync_options='-uahv',
    )
    if new_backup.is_valid():
        repository_backup = backup_repository.BackupRepository(local_psql_session, new_backup)
        for backup in repository_backup.get_backups():
            print(backup)
finally:
    local_psql_session.close()
    server_mysql_session.close()
