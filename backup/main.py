from backup.repositories import os_repository
from entities import backup

new_backup = backup.Backup('Pasta Git', '/home/fernando/git', '/tmp/teste', True, '')

repository_os = os_repository.OsRepository(new_backup)
# repository_os.make_backup()
# print(repository_os.messages)
repository_os.zip_sub_directories()
