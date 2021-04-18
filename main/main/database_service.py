import abc


class DatabaseService(abc.ABC):
    @abc.abstractmethod
    def initial_migration(self):
        pass

    @abc.abstractmethod
    def query(self, query, args=(), one=False):
        pass

    @abc.abstractmethod
    def execute(self, query, args=()):
        pass
