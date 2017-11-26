import sqlite3
import sys
import math
import os
import time
sys.path.insert(0, "..")
from georgiatech import GeorgiaTech
import collect
import sql
from threading import Thread

gt = GeorgiaTech()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../database.db")

thread = Thread(target=collect.run)
thread.start()

def get_colors():
    return gt.route_colors

# Returns the latest bus data for a stop
def get_latest(stop):
    stops = "(" + str(gt.stop_names[stop])[1:-1] + ")"
    query = "SELECT * FROM (SELECT * FROM NEXTBUS where stop in {}) GROUP BY route, stop HAVING MAX(timestamp)".format(str(stops))
    print query
    results = sql.query_read(query)
    # Only include results that occured less thatn 5 mins ago
    results = [x for x in results if  int(time.time()) - x[0] < 200]
    return results

def get_top(stop, route, n):
    query = "SELECT * FROM NEXTBUS where stop=\'{}\' and route = \'{}\' order by timestamp DESC limit {}".format(stop, route, n)
    print query
    return sql.query_read(query)

def get_stop_names():
    return gt.stop_names

def find_closest_stop(lat, lon):
    closest_stop = None
    closest_distance = None
    for key in gt.stop_coords:
        latlon = gt.stop_coords[key]
        dist = math.sqrt((lat-latlon[0])**2 + (lon-latlon[1])**2)
        if closest_distance is None or closest_distance > dist:
            closest_distance = dist
            closest_stop = key[1]
    for key in gt.stop_names:
        if closest_stop in gt.stop_names[key]:
            return key

if __name__ == "__main__":
    print get_top("Recreation Center", "red", 10)