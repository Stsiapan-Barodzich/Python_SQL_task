import argparse
import sys
from db_connection import MySQLConnection
from inserters import RoomInserter, StudentInserter
from data_loader import DataLoader
from queries import QUERIES
from init_db import init_db

def parse_args():
    parser = argparse.ArgumentParser(description="Load JSON data into MySQL and run queries.")
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

        print("Initializing database...")
        init_db()

        config = {
            "host": args.host,
            "user": args.user,
            "password": args.password,
            "database": args.database,
            "port": args.port
        }

        conn = MySQLConnection(config).connect()
        cursor = conn.cursor()

        print("Loading data...")
        loader = DataLoader()
        RoomInserter().insert(cursor, loader.load_json(args.rooms_file))
        StudentInserter().insert(cursor, loader.load_json(args.students_file))
        conn.commit()

        print("Running queries...")
        for name, sql in QUERIES.items():
            print(f"\n--- {name} ---")
            cursor.execute(sql)
            for row in cursor.fetchall():
                print(row)

        cursor.close()
        conn.close()
        print("All tasks completed successfully.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
