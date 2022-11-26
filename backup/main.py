from backup.engines import server_mysql_engine
from engines import local_psql_engine
from entities import backup

from backup.databases import database
from backup.forms import backup_form
from backup.queries import device_query, frequency_query
from backup.repositories import backup_repository, os_repository

psql_engine = local_psql_engine.LocalPsqlEngineConnection()
local_psql_session = psql_engine.make_session()

mysql_engine = server_mysql_engine.ServerMysqlEngineConnection()
server_mysql_session = mysql_engine.make_session()

try:
    # database.create_tables(engine)

    repository_backup = backup_repository.BackupRepository()
    # form_backup = backup_form.BackupForm()
    # new_backup = backup.Backup(
    #     description=input('Nome do backup: '),
    #     origin=form_backup.terminal_directory_check(),
    #     target=form_backup.terminal_directory_check(),
    #     need_compress=form_backup.terminal_boolean_validation(),
    #     rsync_options=form_backup.terminal_rsync_options_are_valid()
    # )
    # repository_backup.create_backup(session, new_backup)

    backup = repository_backup.get_bakcup_by_id(local_psql_session, 3)
    print(backup.origin)
    # backup.origin = '/home/fernando/git/bin'
    # backup.target = '/home/fernando/teste/'
    # backup.rsync_options = '-uahv --delete'
    # repository_backup.update_backup(session, backup)

    # repository_backup.delete_backup(session, backup)
    #
    # repository_os = os_repository.OsRepository(backup)
    # repository_os.make_backup()
    # print(backup)
    # backups = repository_backup.get_backups(session)
    # for backup in backups:
    #     print(backup)

    # query_frequency = frequency_query.FrequencyQuery()
    # frequencies = query_frequency.get_frequencies(session)
    # for frequency in frequencies:
    #     print(frequency)
    #
    # query_device = device_query.DeviceQuery()
    # devices = query_device.get_devices(session)
    # for device in devices:
    #     print(device)
finally:
    local_psql_session.close()
    server_mysql_session.close()
