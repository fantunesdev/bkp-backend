import filecmp
import os
import shutil
from datetime import date, datetime

from backup.entities.backup import Backup


class OsRepository:
    def __init__(self, backup: Backup):
        self.__backup = backup
        self.__messages = ''

    @property
    def messages(self):
        return self.__messages

    def zip_sub_directories(self):
        today = date.today().strftime('%Y-%m-%d')
        initial_directory = os.getcwd()
        os.chdir(self.__backup.origin)
        for sub_directory in self.__backup.sub_directories:
            zip_name = f'{sub_directory}-{today}.tar.bz2'.lower()
            # exclude_directories = self.exclude_directories(sub_directory)
            # bzip_command = f'tar -cjf {zip_name} {self.__backup.origin}/{sub_directory} --exclude {exclude_directories}'
            zip_command = (
                f'tar -cjf {zip_name} {self.__backup.origin}/{sub_directory}'
            )
            os.system(zip_command)
            self.__messages += (
                f'O arquivo {zip_name} foi compactado com sucesso.\n'
            )
        os.chdir(initial_directory)
        self.__messages += '\n'

    def exclude_directories(self):
        exclude_directories = ['venv', '.idea']
        exclude_paths = ''
        for item in self.__backup.get_all_directory_itens():
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
        os.chdir(self.__backup.origin)
        itens = os.listdir(self.__backup.origin)
        for item in itens:
            if 'tar.bz2' in item:
                zip_files.append(item)
            for file in zip_files:
                for sub_directory in self.__backup.sub_directories:
                    if sub_directory.lower() in file:
                        target = (
                            f'{self.__backup.destiny}/{sub_directory}/{file}'
                        )
                        new_dict = {'file': file, 'path': target}
                        if new_dict in targets:
                            pass
                        else:
                            targets.append(new_dict)
        os.chdir(initial_directory)
        return targets

    def move_zip_files(self):
        try:
            initial_directory = os.getcwd()
            os.chdir(self.__backup.origin)
            targets = self.get_targets()
            for target in targets:
                shutil.move(target['file'], target['path'])
                self.__messages += f'O arquivo {target["file"]} foi movido para {target["path"]}.\n'
            os.chdir(initial_directory)
            self.__messages += '\n'
        except FileNotFoundError as error:
            folder = str(error).split('/')[-2]
            os.makedirs(f'{self.__backup.destiny}/{folder}')
            self.move_zip_files()

    def make_backup(self):
        self.__messages += (
            f'Iniciando o backup da pasta "{self.__backup.origin}".\n\n'
        )
        start = datetime.now()
        if self.__backup.need_compress:
            self.zip_sub_directories()
            self.move_zip_files()
            sub_directoryes_lenght = len(self.__backup.sub_directories)
            self.__messages += (
                f'Total de backups realizados: {sub_directoryes_lenght}.\n'
            )
        else:
            command = f'rsync {self.__backup.rsync_options} {self.__backup.origin} {self.__backup.destiny}'
            os.system(command)
        end = datetime.now()
        self.__messages += f'Tempo total: {(end - start).seconds} segundos.'

    def files_are_equal(self, file0, file1):
        path0 = f'{self.__backup.destiny}/{file0}'
        path1 = f'{self.__backup.destiny}/{file1}'
        return filecmp.cmp(path0, path1)
