import sqlite3
import os

def init_database():
    db_name = 'music.db'
    
    # # Remove existing database file if it exists
    # if os.path.exists(db_name):
    #     os.remove(db_name)
    
    # Create a new database and execute SQL script
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Read and execute SQL file
    with open('database.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()

