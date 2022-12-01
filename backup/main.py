from backup.databases import database
from backup.engines import local_psql_engine, server_mysql_engine
from backup.entities.backup import Backup
from backup.repositories import (
    backup_repository,
    frequency_repository,
    os_repository,
)

psql_engine = local_psql_engine.LocalPsqlEngineConnection()
local_psql_session = psql_engine.make_session()

mysql_engine = server_mysql_engine.ServerMysqlEngineConnection()
server_mysql_session = mysql_engine.make_session()

try:
    database.create_tables(psql_engine)
    repository_backup = backup_repository.BackupRepository(local_psql_session)
    repository_frequence = frequency_repository.FrequencyRepository(
        local_psql_session
    )

    backup_db = repository_backup.get_backup_by_id(7)
    backup = Backup(
        description=backup_db.description,
        source=backup_db.source,
        target=backup_db.target,
        program=backup_db.program,
        options=backup_db.options,
        frequency=backup_db.frequency,
    )
    repository_os = os_repository.OsRepository(backup)
    repository_os.make_backup(local_psql_session)

finally:
    local_psql_session.close()
    server_mysql_session.close()
