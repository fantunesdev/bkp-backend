import os


class BackupForm:
    def directory_is_valid(self, directory: str):
        if '\\' in directory:
            directory = directory.replace('\\', '')
        if os.path.exists(directory):
            return True
        raise FileNotFoundError

    def rsync_options_are_valid(self, options: str):
        if options == '':
            return True
        elif options == '-uahv':
            return True
        elif options == '-uahv --delete':
            return True
        else:
            raise ValueError

    def terminal_directory_check(self):
        try:
            directory = input('Diretório de origem: ')
            self.directory_is_valid(directory)
            return directory
        except FileNotFoundError:
            print(
                'Arquivo ou diretório não encontrado. Por favor tente novamente.'
            )
            exit()

    def terminal_boolean_validation(self):
        try:
            need_compress = input('Comprimido (N/s): ')
            if need_compress == '':
                return False
            if need_compress.lower() == 's':
                return True
            if need_compress.lower() == 'n':
                return False
            else:
                raise ValueError
        except ValueError:
            print(
                'Resposta inválida Digite "s" ou "n", ou apenas aperte Enter. Por favor, tente novamente'
            )
            exit()

    def terminal_rsync_options_are_valid(self):
        try:
            rsync_options = input('Digite as opções do rsync: ')
            self.rsync_options_are_valid(rsync_options)
            return rsync_options
        except ValueError:
            print(
                'Resposta inválida Digite "s" ou "n", ou apenas aperte Enter'
            )
            exit()
