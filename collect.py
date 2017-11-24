import xmltodict
import requests
import time
import os
import log
import traceback
from georgiatech import GeorgiaTech
import sqlite3
import os

print("v4")

session = requests.Session()
session.headers.update({"User-Agent": "NextBuzz (nick.petosa@gmail.com)"})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")
conn = sqlite3.connect(db_path)

gt = GeorgiaTech()
header = "timestamp,stop,route,kmperhr,busID,numBuses,busLat,busLong,layover,isDeparture,predictedArrival,secondsToArrival,temperature,pressure,humidity,visibility,weather,wind,cloudCoverage"

while True:
    try:
        time.sleep(5)

        with open("predictions.csv", "a") as file:
            if os.stat("predictions.csv").st_size == 0:
                file.write(header)
                file.write("\n")

        weather = session.get("https://api.openweathermap.org/data/2.5/weather?q=atlanta&APPID=00c4c655fa601a48dc5bf4f34c4ce86a")

        if weather.status_code != 200:
            continue

        weather_json = weather.json()

        for route in gt.all_routes:
            time.sleep(2)
            r = session.get("https://gtbuses.herokuapp.com/agencies/georgia-tech/routes/" + route + "/predictions")
            r2 = session.get("https://gtbuses.herokuapp.com/agencies/georgia-tech/routes/" + route + "/vehicles")

            if r.status_code != 200 or r2.status_code != 200:
                continue
            
            stops = xmltodict.parse(r.text)["body"]["predictions"]
            for stop in stops:
                stop_name = stop["@stopTag"]
                route_name = stop["@routeTag"]

                # First determine if there are any predictions
                if "direction" not in stop:
                    log.log("No predictions for stop " + stop_name + " for route " + route_name)
                    continue
                stop_predictions = stop["direction"]["prediction"]
                if type(stop_predictions) == list:
                    prediction = stop_predictions[0]
                else:
                    prediction = stop_predictions
                
                # Next extract prediction data
                layover = "@affectedByLayover" in prediction
                is_departure = prediction["@isDeparture"] == "true"
                arrival_epoch = int(int(prediction["@epochTime"])/1000)
                seconds_arrival = int(prediction["@seconds"])
                current_epoch = arrival_epoch - seconds_arrival
                bus_number = prediction["@vehicle"]

                # Next extract vehicle data
                vehicles = xmltodict.parse(r2.text)["body"]["vehicle"]
                if type(vehicles) != list:
                    vehicles = [vehicles]
                numbuses = len(vehicles)
                kmperhr = -1
                buslat = -1
                buslong = -1
                for v in vehicles:
                    if bus_number == v["@id"]:
                        kmperhr = v["@speedKmHr"]
                        buslat = v["@lat"]
                        buslong = v["@lon"]

                # Next is weather data
                weather_name = None
                if type(weather_json["weather"]) == list and len(weather_json["weather"]) > 0:
                    weather_name = weather_json["weather"][0]["main"]

                # Build the row
                row = []
                row.append(current_epoch) # Timestamp
                row.append(stop_name) # Stop being approached
                row.append(route_name) # Red, blue...
                row.append(kmperhr) # Speed of bus
                row.append(bus_number) # Bus ID
                row.append(numbuses) # Number of buses
                row.append(buslat) # Latitude of bus
                row.append(buslong) # Longitude of bus
                row.append(layover) # Is this bus' prediction inacurrate?
                row.append(is_departure) # Is the bus waiting?
                row.append(arrival_epoch) # Predicted timestamp of arrival
                row.append(seconds_arrival) # Seconds to arrival prediction
                row.append(weather_json["main"]["temp"]) # Temp in kelvin
                row.append(weather_json["main"]["pressure"]) # Air pressure
                row.append(weather_json["main"]["humidity"]) # Air humidity
                row.append(weather_json["visibility"]) # Air visibility
                row.append(weather_name) # cloudy, rainy, sunny...
                row.append(weather_json["wind"]["speed"]) # Wind speed
                row.append(weather_json["clouds"]["all"]) # Cloud coverage

                output = "("
                for item in row:
                    if isinstance(item, basestring):
                        output += "\'" + str(item) + "\',"
                    else:
                        output += str(item) + ","
                output = output[0: -1]
                output += ")"

                query = "INSERT INTO NEXTBUS VALUES " + output
                print(query)

                c = conn.cursor()
                c.execute(query)

                with open("predictions.csv", "a") as file:
                    file.write(str(row)[1:len(str(row))-1].replace(" ","").replace("\'","") + "\n")

                log.log("Logged for " + route_name + " at " + stop_name)

    except Exception as e:
        log.log("Exception:")
        log.log(traceback.format_exc())
