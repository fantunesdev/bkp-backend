import os

import hvac
from dotenv import load_dotenv
from hvac.exceptions import VaultDown
from sqlalchemy import create_engine

from backup.engines.engine import Engine

load_dotenv()


class ServerMysqlEngineConnection(Engine):
    def connect(self):
        try:
            client = hvac.Client(url=os.getenv('VAULT_URL'))

            os.environ['MYSQL_USER'] = client.kv.v1.read_secret('mysql/user')[
                'data'
            ]['user']
            os.environ['MYSQL_PASSWORD'] = client.kv.v1.read_secret(
                'mysql/password'
            )['data']['password']

            user = os.getenv('MYSQL_USER')
            password = os.getenv('MYSQL_PASSWORD')
            host = os.getenv('MYSQL_HOST')
            database = os.getenv('MYSQL_DB')
            port = os.getenv('MYSQL_PORT')

            database_url = (
                f'mysql://{user}:{password}@{host}:{port}/{database}'
            )

            return create_engine(database_url)

        except VaultDown:
            os.system('vault -u')
            self.connect()
            return None
