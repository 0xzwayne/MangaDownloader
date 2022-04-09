from multiprocessing import connection
from pathlib import Path
import sqlite3

dbpath = f"{Path(__file__).parents[1]}\data\database.db"

def connect(dbpath):
    connection = sqlite3.connect(dbpath)
    cursor = cursor = connection.cursor()
    return connection,cursor

def update(data):
    connection, cursor = connect(dbpath)
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Mangas
              (name TEXT, url TEXT)''')
    connection.commit()
    
    for i in data:
        #print(i["name"],i["url"])
        sqlquery = f'''INSERT INTO Mangas(name, url) VALUES("{i["name"].replace('"',"")}","{i["url"]}")'''
        cursor.execute(sqlquery)
        connection.commit()
    cursor.close()
    connection.close()
    
def search(query):
    connection, cursor = connect(dbpath)
    
    sqlquery = f"""SELECT * FROM Mangas WHERE name LIKE '%{query}%'"""
    cursor.execute(sqlquery)
    rows = cursor.fetchall()
    return rows

    
    
if __name__ == "__main__":
    results = search("one piece")
    print([result[0] for result in results])