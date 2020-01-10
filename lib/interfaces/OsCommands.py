import abc


class OsCommands(abc.ABCMeta):

    @abc.abstractmethod
    def get_os(self):
        pass

    @abc.abstractmethod
    def get_ram(self):
        pass

    @abc.abstractmethod
    def get_hard_disk(self):
        pass
