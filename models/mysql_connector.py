import mysql.connector
from config import db_config

def execute_query(query, params=None):
    cnx = mysql.connector.connect(**db_config)  # use **db_config 
    cursor = cnx.cursor()
    cursor.execute(query, params) if params else cursor.execute(query)
    results = []
    for record in cursor:
        results.append(record)
    cnx.commit() 
    last_id = cursor.lastrowid
    cnx.close()
    if "insert" in query.lower():  #use lower() 
        return last_id
    return results