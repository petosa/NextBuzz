import datetime
import time

def log(s):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')    
    with open("system.log", "a") as file:
        file.write("[" + st + "] " + str(s) + "\n")