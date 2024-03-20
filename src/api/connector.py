import http.client
import src.constants.constants as constants

from abc import ABC, abstractmethod

class Connector:
    def __init__(self, config) -> None:
        match config:
            case constants.FOOTBALL:
                self.connection = Connection_Football()

    def connect(self):
        return self.connection.get_or_create_connection()



class Connection(ABC):
    def __init__(self) -> None:
        self.connection = None

    def get_or_create_connection(self):
        # Avoid recreating the connection
        if self.connection is None:
            self.connection = self.create_connection()
        
        # Return the connection
        return self.connection
    
    @abstractmethod
    def create_connection(self):
        pass
    
class Connection_Football(Connection):
    def create_connection(self):
        return http.client.HTTPSConnection(constants.FOOTBALL_API)