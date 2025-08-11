from abc import ABC, abstractmethod

class DataInserter(ABC):
    @abstractmethod
    def insert(self, cursor, data: list):
        pass

class RoomInserter(DataInserter):
    def insert(self, cursor, data: list):
        for item in data:
            cursor.execute("INSERT INTO rooms (id, name) VALUES (%s, %s)", 
                          (item["id"], item["name"]))

class StudentInserter(DataInserter):
    def insert(self, cursor, data: list):
        for item in data:
            cursor.execute(
                "INSERT INTO students (id, name, sex, birthday, room_id) VALUES (%s, %s, %s, %s, %s)",
                (item["id"], item["name"], item["sex"], item["birthday"], item["room"])
            )
            