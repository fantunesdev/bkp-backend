import filecmp
import os
import subprocess
from datetime import date, datetime

from backup.entities import relatory
from backup.entities.backup import Backup
from backup.repositories import backup_repository, relatory_repository


class OsRepository:
    def __init__(self, backup: Backup):
        """Construtor da classe OsRepository."""
        self.backup = backup
        self.__messages = ''
        self.today = date.today().strftime('%Y-%m-%d')
        self.relatory = relatory.Relatory()

    @property
    def messages(self):
        return self.__messages

    def compress_file_wont_be_empy(self):
        itens = os.listdir(self.backup.source)
        files = []
        for item in itens:
            is_directory = os.path.isdir(f'{self.backup.source}/{item}')
            if not is_directory:
                files.append(item)
        if len(files) == 0:
            return False
        return True

    def make_backup(self, session):
        match self.backup.program:
            case 'rsync':
                self.rsync_backup()
            case 'tar':
                self.tar_backup()
            case 'mysqldump':
                self.mysql_backup()
        repository_relatory = relatory_repository.RelatoryRepository(session)
        repository_backup = backup_repository.BackupRepository(
            session, self.backup
        )
        backup_db = repository_backup.get_backup_by_description_and_frequency(
            self.backup
        )
        self.relatory.backup = backup_db
        repository_relatory.create_relatory(self.relatory)

    def tar_backup(self):
        self.__messages += (
            f'Iniciando o backup da pasta "{self.backup.source}":\n'
        )
        start = datetime.now()

        self.compress_directory()

        total_backups = len(self.backup.sub_directories)
        if self.compress_file_wont_be_empy():
            total_backups += 1
        elif self.backup.sub_directories == '.':
            total_backups -= 1
        self.__messages += f'\nTotal de backups realizados: {total_backups}.\n'
        end = datetime.now()
        self.__messages += f'Tempo total: {(end - start).seconds} segundos.'
        self.relatory.log = self.messages

    def compress_directory(self):
        initial_directory = os.getcwd()
        os.chdir(self.backup.source)
        status_list = []

        if self.compress_file_wont_be_empy():
            self.compress_root_directory(status_list)
        elif self.backup.sub_directories != '.':
            self.compress_sub_directories(status_list)

        if False in status_list:
            self.relatory.status = False
        else:
            self.relatory.status = True

        os.chdir(initial_directory)

    def compress_root_directory(self, status_list: list):
        exclude = ''
        self.__messages += f'\nCompactando diretório {self.backup.source}: '
        for directory in self.backup.sub_directories:
            exclude += f'--exclude={directory} '
        file_name = (
            f'{self.backup.source.split("/")[-1]}-{self.today}.tar.bz2'.lower()
        )
        self.backup.command = f'tar -cjf /tmp/{file_name} {exclude} .'
        param = self.backup.command.split(' ')
        with subprocess.Popen(param) as command:
            self.get_console_response(command)
            self.move_file(f'/tmp/{file_name}', self.backup.target)
            status = os.path.isfile(f'{self.backup.target}/{file_name}')
            status_list.append(status)

    def compress_sub_directories(self, status_list: list):
        for sub_directory in self.backup.sub_directories:
            self.__messages += f'\nCompactando diretório {self.backup.source}/{sub_directory}: '
            file_name = f'{sub_directory}-{self.today}.tar.bz2'.lower()
            compress_command = f'tar -cjf /tmp/{file_name} {sub_directory}'
            param = compress_command.split(' ')
            with subprocess.Popen(param) as command:
                self.get_console_response(command)
                self.move_file(
                    f'/tmp/{file_name}',
                    f'{self.backup.target}/{sub_directory}/',
                )
                status = os.path.isfile(
                    f'{self.backup.target}/{sub_directory}/{file_name}'
                )
                status_list.append(status)

    def get_targets(self):
        targets = []
        zip_files = []
        initial_directory = os.getcwd()
        os.chdir(self.backup.source)
        itens = os.listdir(self.backup.source)
        for item in itens:
            if 'tar.bz2' in item:
                zip_files.append(item)
            for file in zip_files:
                for sub_directory in self.backup.sub_directories:
                    if sub_directory.lower() in file:
                        target = f'{self.backup.target}/{sub_directory}/{file}'
                        new_dict = {'file': file, 'path': target}
                        if new_dict in targets:
                            pass
                        else:
                            targets.append(new_dict)
        os.chdir(initial_directory)
        return targets

    def move_file(self, source: str, target: str):
        try:
            self.__messages += f'Movendo {source} para {self.backup.source}:'
            if not os.path.isdir(target):
                raise FileNotFoundError
            with subprocess.Popen(['mv', source, target]) as command:
                self.get_console_response(command)
        except FileNotFoundError:
            os.makedirs(target)
            self.move_file(source, target)

    def rsync_backup(self):
        subprocess_command_param = self.backup.command.split(' ')
        subprocess_command_param.append(self.backup.source)
        subprocess_command_param.append(self.backup.target)
        with subprocess.Popen(
            subprocess_command_param, stdout=subprocess.PIPE, shell=False
        ) as command:
            self.get_console_response(command)
        self.relatory.log = self.messages

    def mysql_backup(self):
        param = self.backup.command.replace('"', '').split(' ')
        param.pop()
        with open(self.backup.target, 'w', encoding='utf-8') as dumpfile:
            with subprocess.Popen(param, stdout=dumpfile) as command:
                output, error = command.communicate()
                if output:
                    self.__messages = output.decode('UTF-8')
                    self.relatory.status = True
                else:
                    if error:
                        self.__messages = error.decode('UTF-8')
                        self.relatory.status = False
                    else:
                        self.__messages = (
                            f'Backup {self.backup} realizado com sucesso!'
                        )
                        self.relatory.status = True
                    dumpfile.close()
        self.relatory.log = self.messages

    def get_console_response(self, command: subprocess.Popen):
        output, error = command.communicate()
        if output:
            self.relatory.status = True
            self.__messages += 'SUCESSO!\n'
            self.__messages += output.decode('UTF-8')
        else:
            if error:
                self.relatory.status = False
                self.__messages += 'FALHOU!\n'
                self.__messages += error.decode('UTF-8')
            else:
                self.relatory.status = True
                self.__messages += 'SUCESSO!\n'

    def exclude_directories(self):
        exclude_directories = ['venv', '.idea']
        exclude_paths = ''
        for item in self.backup.get_all_directory_itens():
            for directory in exclude_directories:
                if directory in item:
                    path = item.split(directory)
                    full_path = f'{path[0]}{directory}'
                    if full_path in exclude_paths:
                        pass
                    else:
                        exclude_paths += f'"{full_path}" '
        return exclude_paths

    def files_are_equal(self, file0):
        return filecmp.cmp(file0, self.backup.target)
