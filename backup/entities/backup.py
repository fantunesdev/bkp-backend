import os

from backup.databases import database


class Backup:

    def __init__(
        self, description, source, target, program, options, frequency
    ):
        """Método construtor da classe Backup."""
        self.description = description
        self.source = source
        self.__target = target
        self.program = program
        self.options = options
        self.frequency = frequency
        self.__command = self.__set_command()

    def __str__(self):
        return self.description

    def __eq__(self, other):
        return self.source == other.source and self.target == other.target

    def __ne__(self, other):
        return self.source != other.source or self.target != other.target

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value: str):
        if self.directory_is_valid(value):
            self.__target = value
        else:
            raise FileNotFoundError

    @property
    def command(self):
        return self.__command

    @property
    def sub_directories(self):
        itens = os.listdir(self.source)
        directories = []
        for item in itens:
            is_directory = os.path.isdir(f'{self.source}/{item}')
            if is_directory:
                directories.append(item)
        if len(directories) == 0:
            directories.append('.')
        return directories

    def __set_command(self):
        if self.program == 'mysqldump':
            return f'{self.program} {self.options} {self.source} > {self.target}'
        else:
            return f'{self.program} {self.options} "{self.source}" "{self.target}"'

    def convert(self, backup: database.Backup):
        self.description = backup.description
        self.source = backup.source
        self.__target = backup.target
        self.program = backup.program
        self.options = backup.options
        self.frequency = backup.frequency
        self.__command = self.__set_command()
        return self

    def is_valid(self):
        validations = [
            self.directory_is_valid(self.source),
            self.directory_is_valid(self.__target)
        ]
        for validation in validations:
            if not validation:
                return False
        return True

    def directory_is_valid(self, directory: str):
        if '\\' in directory:
            directory = directory.replace('\\', '')
        if os.path.exists(directory):
            return True
        if self.source == directory:
            print('Diretório de origem não encontrado.')
        if self.target == directory:
            print('Diretório de destino não encontrado')

    def validate_directory(self, diretory: str):
        if self.directory_is_valid(diretory):
            return diretory
        raise FileNotFoundError

    def get_all_directory_itens(self, *args):
        if args:
            directory = args[0]
            new_itens_list = args[1]
        else:
            new_itens_list = []
            directory = self.source

        itens = os.listdir(directory)

        for item in itens:
            is_directory = os.path.isdir(f'{directory}/{item}')
            path = f'{directory}/{item}'
            new_itens_list.append(path)
            if is_directory:
                new_directory = f'{directory}/{item}'
                self.get_all_directory_itens(new_directory, new_itens_list)
        return new_itens_list
