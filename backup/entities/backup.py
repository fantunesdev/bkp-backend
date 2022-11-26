import os


class Backup:
    def __init__(
        self, description, origin, target, need_compress, rsync_options
    ):
        """Método construtor da classe Backup."""
        self.__desciption = description
        self.__origin = origin
        self.__target = target
        self.__need_compress = need_compress
        self.__rsync_options = rsync_options

    def __str__(self):
        return self.__desciption

    def __eq__(self, other):
        return (
            self.__origin == other.__origin and self.__target == other.__target
        )

    def __ne__(self, other):
        return (
            self.__origin != other.__origin or self.__target != other.__target
        )

    @property
    def description(self):
        return self.__desciption

    @property
    def origin(self):
        return self.__origin

    @property
    def target(self):
        return self.__target

    @property
    def need_compress(self):
        return self.__need_compress

    @property
    def rsync_options(self):
        return self.__rsync_options

    @property
    def sub_directories(self):
        itens = os.listdir(self.__origin)
        directories = []
        for item in itens:
            is_directory = os.path.isdir(f'{self.__origin}/{item}')
            if is_directory:
                directories.append(item)
        return directories

    def get_all_directory_itens(self, *args):
        if args:
            directory = args[0]
            new_itens_list = args[1]
        else:
            new_itens_list = []
            directory = self.origin

        itens = os.listdir(directory)

        for item in itens:
            is_directory = os.path.isdir(f'{directory}/{item}')
            path = f'{directory}/{item}'
            new_itens_list.append(path)
            if is_directory:
                new_directory = f'{directory}/{item}'
                self.get_all_directory_itens(new_directory, new_itens_list)
        return new_itens_list
