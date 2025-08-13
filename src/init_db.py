from db_connection import MySQLConnection

def init_db():
    schema_sql = """
    CREATE DATABASE python_json_schema;
    USE python_json_schema;

    CREATE TABLE rooms(
        id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );

    CREATE TABLE students(
        id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        sex CHAR(1) NOT NULL,
        birthday DATE NOT NULL,
        room_id INT NOT NULL,
        FOREIGN KEY(room_id) REFERENCES rooms(id)
    );

    CREATE INDEX idx_room_id ON students(room_id);
    CREATE INDEX idx_birthday ON students(birthday);
    CREATE INDEX idx_sex ON students(sex);
    """
    conn = MySQLConnection({
        "host": "localhost",
        "user": "root",
        "password": "root",
        "port": 3307
    }).connect()

    cursor = conn.cursor()
    for statement in schema_sql.strip().split(";"):
        if statement.strip():
            cursor.execute(statement)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()
