import filecmp
import os
import shutil
import subprocess
from datetime import date, datetime

from backup.entities import relatory
from backup.entities.backup import Backup
from backup.repositories import relatory_repository, backup_repository


class OsRepository:
    def __init__(self, backup: Backup):
        """Construtor da classe OsRepository."""
        self.backup = backup
        self.__messages = ''

    @property
    def messages(self):
        return self.__messages

    def zip_sub_directories(self, new_relatory: relatory.Relatory):
        today = date.today().strftime('%Y-%m-%d')
        initial_directory = os.getcwd()
        os.chdir(self.backup.source)
        for sub_directory in self.backup.sub_directories:
            if self.backup.sub_directories[0] == '.':
                file_name = self.backup.source.split('/')[-1]
            else:
                file_name = sub_directory
            zip_name = f'{file_name}-{today}.tar.bz2'.lower()
            zip_command = (
                f'tar -cjf {zip_name} {self.backup.source}/{sub_directory}'
            )
            os.system(zip_command)
            path_file = os.path.isdir(f'{self.backup.source}/{file_name}')
            if os.path.isfile(path_file):
                self.__messages += (
                    f'O arquivo {zip_name} foi compactado com sucesso.\n'
                )
                new_relatory.status = True
            else:
                self.__messages += (
                    f'Houve um erro na compactação do arquivo{zip_name}.\n'
                )
                new_relatory.status = False
            new_relatory.log = self.messages
        os.chdir(initial_directory)
        self.__messages += '\n'

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
                        target = (
                            f'{self.backup.target}/{sub_directory}/{file}'
                        )
                        new_dict = {'file': file, 'path': target}
                        if new_dict in targets:
                            pass
                        else:
                            targets.append(new_dict)
        os.chdir(initial_directory)
        return targets

    def move_zip_files(self, new_relatory: relatory.Relatory):
        try:
            initial_directory = os.getcwd()
            os.chdir(self.backup.source)
            targets = self.get_targets()
            for target in targets:
                shutil.move(target['file'], target['path'])
                path_file = os.path.isdir(f'{self.backup.source}/{target["file"]}')
                if os.path.isfile(path_file):
                    new_relatory.status = True
                    self.__messages += f'O arquivo {target["file"]} foi movido para {target["path"]}.\n'
                else:
                    self.__messages += f'Ocorreu um erro ao mover {target["file"]} para {target["path"]}.\n'
                    new_relatory.status = False
                new_relatory.log += self.messages
            os.chdir(initial_directory)
            self.__messages += '\n'
        except FileNotFoundError as error:
            folder = str(error).split('/')[-2]
            os.makedirs(f'{self.backup.target}/{folder}')
            self.move_zip_files(new_relatory)

    def make_backup(self, session):
        new_relatory = relatory.Relatory(backup=self.backup)
        match self.backup.program:
            case 'rsync':
                self.rsync_backup(new_relatory)
            case 'tar':
                self.tar_backup(new_relatory)
            case 'mysqldump':
                self.mysql_backup(new_relatory)
        repository_relatory = relatory_repository.RelatoryRepository(session)
        repository_backup = backup_repository.BackupRepository(session, self.backup)
        backup_db = repository_backup.get_backup_by_description_and_frequency(self.backup)
        new_relatory.backup = backup_db
        repository_relatory.create_relatory(new_relatory)

    def tar_backup(self, new_relatory: relatory.Relatory):
        self.__messages += (
            f'Iniciando o backup da pasta "{self.backup.source}".\n\n'
        )
        start = datetime.now()

        self.zip_sub_directories(new_relatory)
        self.move_zip_files()

        sub_directoryes_lenght = len(self.backup.sub_directories)
        self.__messages += (
            f'Total de backups realizados: {sub_directoryes_lenght}.\n'
        )
        end = datetime.now()
        self.__messages += f'Tempo total: {(end - start).seconds} segundos.'

    def rsync_backup(self, new_relatory: relatory.Relatory):
        subprocess_command_param = self.backup.command.split(' ')
        for index in range(1):
            subprocess_command_param.pop()
        subprocess_command_param.append(self.backup.source)
        subprocess_command_param.append(self.backup.target)
        command = subprocess.Popen(
            subprocess_command_param, stdout=subprocess.PIPE, shell=False
        )
        output, error = command.communicate()
        if output:
            new_relatory.status = True
            self.__messages = output.decode('UTF-8')
        else:
            if error:
                new_relatory.status = False
                self.__messages = error.decode('UTF-8')
        new_relatory.log = self.messages

    def mysql_backup(self, new_relatory: relatory.Relatory):
        param = self.backup.command.replace('"', '').split(' ')
        param.pop()
        with open(self.backup.target, 'w') as dumpfile:
            command = subprocess.Popen(param, stdout=dumpfile)
            output, error = command.communicate()
            if output:
                self.__messages = output.decode('UTF-8')
                new_relatory.status = True
            else:
                if error:
                    self.__messages = error.decode('UTF-8')
                    new_relatory.status = False
                else:
                    self.__messages = f'Backup {self.backup} realizado com sucesso!'
                    new_relatory.status = True
                dumpfile.close()
        new_relatory.log = self.messages

    def files_are_equal(self, file0):
        return filecmp.cmp(file0, self.backup.target)
