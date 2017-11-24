import sqlite3
import sys
sys.path.insert(0, "..")
from georgiatech import GeorgiaTech
import math
import os

gt = GeorgiaTech()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../database.db")
conn = sqlite3.connect(db_path)

# Returns the latest bus data for a stop
def get_latest(stop):
    res = []
    stops = "(" + str(gt.stop_names[stop])[1:-1] + ")"
    for route in gt.all_routes:
        c = conn.cursor()
        query = "SELECT * FROM NEXTBUS WHERE route=\'{}\' and stop IN {} ORDER BY timestamp DESC LIMIT 1".format(route, str(stops))
        print query
        result = c.execute(query)
        row = next(result, None)
        if row:
            res.append(row)
    return res

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
    print get_latest("Recreation Center")