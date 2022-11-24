import engine as engine_file
from entities import backup

from backup.databases import database
from backup.queries import device_query, frequency_query
from backup.repositories import os_repository

new_backup = backup.Backup(
    'Pasta Git', '/home/fernando/git', '/tmp/teste', True, ''
)

repository_os = os_repository.OsRepository(new_backup)


engine = engine_file.EngineConnection()
session = engine.make_session()
try:
    query_frequency = frequency_query.FrequencyQuery()
    frequencies = query_frequency.get_frequencies(session)
    for frequency in frequencies:
        print(frequency)

    query_device = device_query.DeviceQuery()
    devices = query_device.get_devices(session)
    for device in devices:
        print(device)
    # database.create_tables(engine)
finally:
    session.close()
