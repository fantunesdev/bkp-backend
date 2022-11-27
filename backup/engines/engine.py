import abc

from sqlalchemy.orm import sessionmaker


class Engine(abc.ABC):
    @classmethod
    def connect(self):
        ...

    def make_session(self):
        connection = self.connect()
        Session = sessionmaker()
        Session.configure(bind=connection, autoflush=False)
        return Session()
