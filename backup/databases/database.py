from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Backup(Base):
    __tablename__ = 'backup'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    description = Column(String(50))
    origin = Column(String(200))
    target = Column(String(200))
    need_compress = Column(Boolean, nullable=False)
    rsync_options = Column(String(20))

    def __repr__(self):
        return self.description


class Frequency(Base):
    __tablename__ = 'frequency'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False)

    def __repr__(self):
        return self.description


class Relatory(Base):
    __tablename__ = 'relatory'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    backup = Column('Backup', ForeignKey('backup.id'))
    status = Column(Boolean, nullable=False)
    frequency = Column('Frequency', ForeignKey('frequency.id'))
    date = Column(DateTime)
    log = Column(String)

    def __repr__(self):
        return f'{self.date}{self.backup}'


class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(40), nullable=False)
    name = Column(String(20), nullable=False)
    label = Column(String(30))
    mount_point = Column(String(200))
    type = Column(String(30))
    options = Column(String(30))

    def __repr__(self):
        return self.name


def create_tables(engine):
    engine_creator = engine.connect()
    Base.metadata.create_all(engine_creator)
