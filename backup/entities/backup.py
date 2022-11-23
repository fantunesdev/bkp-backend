import os


class Backup:
    def __init__(self, description, origin, destiny, need_compress, rsync_options):
        self.__desciption = description
        self.__origin = origin
        self.__destiny = destiny
        self.__need_compress = need_compress
        self.__rsync_options = rsync_options
        self.__sub_directories = None

    @property
    def description(self):
        return self.__desciption

    @property
    def origin(self):
        return self.__origin

    @property
    def destiny(self):
        return self.__destiny

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
