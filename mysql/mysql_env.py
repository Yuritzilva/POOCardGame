#This code will help to execute queries throught the program execution

# ---- IMPORTS ----
import sys
import os
#we need to append this line so db_connection can be pulled from the src file
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src')) 
from db_connection import get_conn

#First connection to the database, we will try to use the database
def use_DB(conn):
    query = """use CardGame"""
    
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print("Se usará CardGame como base de datos 0_0")
    cursor.close()

def main():
    conn = get_conn()

    if conn:
        use_DB(conn)
        conn.close()
    else:
        print("no se puede usar la BD")
        
if __name__ == "__main__":
    main()