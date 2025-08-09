import json
import mysql.connector
from abc import ABC, abstractmethod

# DB connection interface
class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

class MySQLConnection(DatabaseConnection):
    def __init__(self, config):
        self.config = config

    def connect(self):
        return mysql.connector.connect(**self.config)

# Data insertion interface
class DataInserter(ABC):
    @abstractmethod
    def insert(self, cursor, data):
        pass

class RoomInserter(DataInserter):
    def insert(self, cursor, data):
        for item in data:
            cursor.execute("INSERT INTO rooms (id, name) VALUES (%s, %s)", (item["id"], item["name"]))

class StudentInserter(DataInserter):
    def insert(self, cursor, data):
        for item in data:
            cursor.execute(
                "INSERT INTO students (id, name, sex, birthday, room_id) VALUES (%s, %s, %s, %s, %s)",
                (item["id"], item["name"], item["sex"], item["birthday"], item["room"])
            )

# Loads JSONs
def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# Data processing
def process_data(db_connection, inserters, data_files):
    conn = db_connection.connect()
    cursor = conn.cursor()
    try:
        for inserter, data_file in zip(inserters, data_files):
            data = load_json(data_file)
            inserter.insert(cursor, data)
        conn.commit()
        print("Data loaded successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Сonnection settings
config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "python_json_schema",
    "port": 3307
}

if __name__ == "__main__":
    db_connection = MySQLConnection(config)
    inserters = [RoomInserter(), StudentInserter()]
    data_files = ["rooms.json", "students.json"]
    process_data(db_connection, inserters, data_files)