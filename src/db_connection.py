from abc import ABC, abstractmethod
import mysql.connector

class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

class MySQLConnection(DatabaseConnection):
    def __init__(self, config: dict):
        self.config = config

    def connect(self):
        return mysql.connector.connect(**self.config)
    