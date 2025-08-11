import argparse
import sys
from db_connection import MySQLConnection
from inserters import RoomInserter, StudentInserter
from data_loader import DataLoader

def parse_args():
    parser = argparse.ArgumentParser(description="Loads JSON data into MySQL database.")
    parser.add_argument("rooms_file", help="Path to rooms JSON file")
    parser.add_argument("students_file", help="Path to students JSON file")
    parser.add_argument("--host", default="localhost", help="Database host")
    parser.add_argument("--user", default="root", help="Database user")
    parser.add_argument("--password", default="root", help="Database password")
    parser.add_argument("--database", default="python_json_schema", help="Database name")
    parser.add_argument("--port", type=int, default=3307, help="Database port")
    return parser.parse_args()

def main():
    try:
        args = parse_args()
        config = {
            "host": args.host,
            "user": args.user,
            "password": args.password,
            "database": args.database,
            "port": args.port
        }
        db_connection = MySQLConnection(config)
        loader = DataLoader()
        inserters = [RoomInserter(), StudentInserter()]
        data_files = [args.rooms_file, args.students_file]
        
        conn = db_connection.connect()
        cursor = conn.cursor()
        try:
            for inserter, data_file in zip(inserters, data_files):
                data = loader.load_json(data_file)
                inserter.insert(cursor, data)
            conn.commit()
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    