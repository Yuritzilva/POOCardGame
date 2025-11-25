#This code will help to execute queries throught the program execution to create the base structure of the database

# ---- IMPORTS ----
import sys
import os
import mysql.connector
#we need to append this line so db_connection can be pulled from the src file
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src')) 
from db_connection import get_conn

def create_database(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS CardGame")
        cursor.execute("USE CardGame")
        print("Database is ready :)")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()


def execute_sql_file(conn, filename= None):
   
    if filename is None:
        filename = os.path.join("mysql", "structure.sql")

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' wasn't found")
        return
        
    cursor = conn.cursor()
    
    try:
        with open(filename, 'r') as f:
            
            sql_script = f.read()
            
            # Divide scripts using ; and ignore comments
            commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip() and not cmd.strip().startswith('--')]

            success_count = 0
            for command in commands:
                try:
                    cursor.execute(command)
                    success_count += 1
                except mysql.connector.Error as err:
                    print(f"Failed querie: {command[:50]}...")
                    print(f"   Error: {err}")
                    
            conn.commit()
            print(f"Execution finished, queries executed: {success_count}")

    except Exception as e:
        print(f"Lecture error in SQL file: {e}")
        conn.rollback() # Revert
    finally:
        cursor.close()

def main():
    conn = get_conn()

    if conn:
        create_database(conn)
        file_path = os.path.join("mysql", "structure.sql")
        execute_sql_file(conn, file_path)
        
        print("\n----SHOW TABLES FOR CARD GAME-----")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        print(cursor.fetchall())
        conn.close()

        
if __name__ == "__main__":
    main()