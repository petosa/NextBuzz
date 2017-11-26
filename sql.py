import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

# Wraps all queries to the sqlite db
def query_write(query):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()

def query_read(query):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    result = c.execute(query)
    res = []
    row = next(result, None)
    while row:
        res.append(row)
        row = next(result, None)
    conn.close()
    return res

# Creates the sqlite database, the NEXTBUS table, and builds index
# if none of that already exists.
def create_table():
    query1 = """CREATE TABLE IF NOT EXISTS NEXTBUS (
                                        timestamp integer,
                                        stop text,
                                        route text,
                                        kmperhr text,
                                        busID text,
                                        numBuses text,
                                        busLat text,
                                        busLong text,
                                        layover text,
                                        isDeparture text,
                                        predictedArrival text,
                                        secondsToArrival text,
                                        temperature text,
                                        pressure text,
                                        humidity text,
                                        visibility text,
                                        weather text,
                                        wind text,
                                        cloudCoverage text,
                                        prediction text
                                    );
                            """
    query2 = "CREATE INDEX stop_index ON NEXTBUS (stop);"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(query1)
    try: # Ignore error (index has already been built)                 
        c.execute(query2)  
    except:
        pass
    conn.commit()
    conn.close()                              
