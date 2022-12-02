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
    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    description = Column(String(50))
    source = Column(String(255))
    target = Column(String(255), nullable=False)
    program = Column(String(25), nullable=False)
    options = Column(String(255))
    frequency = Column('frequency', ForeignKey('frequency.id'))

    def __repr__(self):
        """Retorno padrão da classe Backup."""
        return self.description

    def __eq__(self, other):
        """Verifica se dois objetos desta classe são iguais."""
        return self.source == other.source and self.target == other.target

    def __ne__(self, other):
        """Verifica se dois objetos desta classe são diferentes."""
        return self.source != other.source or self.target != other.target


class Frequency(Base):
    __tablename__ = 'frequency'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    description = Column(String(50), nullable=False)

    def __repr__(self):
        """Retorno padrão da classe Frequency."""
        return self.description


class Relatory(Base):
    __tablename__ = 'relatory'
    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    backup = Column('Backup', ForeignKey('backup.id'))
    status = Column(Boolean, nullable=False)
    date = Column(DateTime)
    log = Column(String)

    def __repr__(self):
        """Retorno padrão da classe Relatory."""
        return f'Data: {self.date} - Backup: {self.backup}'

    def __eq__(self, other):
        """Verifica se dois objetos desta classe são iguais."""
        return self.backup == other.backup and self.status == other.status

    def __ne__(self, other):
        """Verifica se dois objetos desta classe são iguais."""
        return self.backup != other.backup and self.status != other.status


class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    uuid = Column(String(40), nullable=False)
    name = Column(String(20), nullable=False)
    label = Column(String(30))
    mount_point = Column(String(255))
    type = Column(String(30))
    options = Column(String(30))

    def __repr__(self):
        """Retorno padrão da classe Device."""
        return self.name


def create_tables(engine):
    engine_creator = engine.connect()
    Base.metadata.create_all(engine_creator)
