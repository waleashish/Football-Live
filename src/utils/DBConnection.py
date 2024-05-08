import psycopg2
import time

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DBConnection(metaclass=SingletonMeta):
    connection = None

    def __init__(self):
        if self.connection is None:
            while True:
                try:
                    self.connection = psycopg2.connect(
                        dbname="football",
                        user="football",
                        password="football",
                        host="postgres-football"
                    )
                    break
                except psycopg2.OperationalError:
                    time.sleep(1)

    def get_connection(self):
        return self.connection
    
    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None