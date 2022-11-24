import os

import hvac
from dotenv import load_dotenv
from hvac.exceptions import VaultDown
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


class EngineConnection:
    def connect(self):
        try:
            client = hvac.Client(url=os.getenv('VAULT_URL'))

            os.environ['POSTGRESQL_USER'] = client.kv.v1.read_secret('postgresql/user')['data']['user']
            os.environ['POSTGRESQL_PASSWORD'] = client.kv.v1.read_secret('postgresql/password')['data']['password']
            user = os.getenv('POSTGRESQL_USER')
            password = os.getenv('POSTGRESQL_PASSWORD')
            database = os.getenv('DATABASE')
            host = os.getenv('HOST')
            port = os.getenv('PORT')
            database_url = f'postgresql://{user}:{password}@{host}:{port}/{database}'

            return create_engine(database_url)
        except VaultDown:
            os.system('vaultctl -u')
            self.connect()

    def make_session(self):
        connection = self.connect()
        Session = sessionmaker()
        Session.configure(bind=connection, autoflush=False)
        return Session()
