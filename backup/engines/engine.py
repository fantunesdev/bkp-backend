from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Engine:
    def connect(self):
        pass

    def make_session(self):
        connection = self.connect()
        Session = sessionmaker()
        Session.configure(bind=connection, autoflush=False)
        return Session()
