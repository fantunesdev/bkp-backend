import os


class Backup:
    def __init__(
        self, description, source, target, need_compress, rsync_options
    ):
        """Método construtor da classe Backup."""
        self.description = description
        self.__source = source
        self.__target = target
        self.__need_compress = need_compress
        self.__rsync_options = rsync_options

    def __str__(self):
        return self.description

    def __eq__(self, other):
        return self.source == other.source and self.target == other.target

    def __ne__(self, other):
        return self.source != other.source or self.target != other.target

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        if self.directory_is_valid(value):
            self.__source = value
        else:
            raise FileNotFoundError

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
    def need_compress(self):
        return self.__need_compress

    @need_compress.setter
    def need_compress(self, value: bool):
        if isinstance(value, bool):
            self.__need_compress = value
        raise ValueError

    @property
    def rsync_options(self):
        return self.__rsync_options

    @rsync_options.setter
    def rsync_options(self, value):
        if self.rsync_options_are_valid():
            self.__rsync_options = value
        else:
            raise ValueError

    @property
    def sub_directories(self):
        itens = os.listdir(self.__source)
        directories = []
        for item in itens:
            is_directory = os.path.isdir(f'{self.__source}/{item}')
            if is_directory:
                directories.append(item)
        if len(directories) == 0:
            directories.append('.')
        return directories

    def is_valid(self):
        validations = [
            self.directory_is_valid(self.__source),
            self.directory_is_valid(self.__target),
            self.need_compress_is_boolean(),
            self.rsync_options_are_valid(),
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
        return False

    def need_compress_is_boolean(self):
        if isinstance(self.need_compress, bool):
            return True
        print('Needcompress não é um booleano.')
        return False

    def rsync_options_are_valid(self):
        valid_options = ['-uahv', '--delete', '--safe-links']
        for option in valid_options:
            if self.__rsync_options == '':
                return True
            if option in self.__rsync_options:
                return True
            print('Opções inválidas do rsync')
            return False

    def validate_directory(self, diretory: str):
        if self.directory_is_valid(diretory):
            return diretory
        raise FileNotFoundError

    def validate_rsync_options(self, rsync_options: str):
        if self.rsync_options_are_valid():
            return rsync_options
        raise ValueError

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
