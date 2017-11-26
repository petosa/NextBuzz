import xmltodict
import requests
import time
import os
import log
import traceback
import sqlite3
import sql
import predict
from georgiatech import GeorgiaTech
from sklearn.externals import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")

def run():
    print("v4") # Print current iteration/version for sanity

    session = requests.Session() # Construct a NextBus API compliant requester
    session.headers.update({"User-Agent": "NextBuzz (nick.petosa@gmail.com)"})

    model = joblib.load(model_path) # Load in the regression model
    sql.create_table() # Create database infra
    gt = GeorgiaTech() # Instatiate context object

    while True: # Big loop for scraping bus data.
        try:
            time.sleep(5) # Pause between requests

            # Collect weather data
            weather = session.get("https://api.openweathermap.org/data/2.5/weather?q=atlanta&APPID=00c4c655fa601a48dc5bf4f34c4ce86a")
            if weather.status_code != 200: # Restart loop if we can't get weather data.
                continue
            weather_json = weather.json()

            # Collect and parse NextBus data
            for route in gt.all_routes:
                time.sleep(2) # Pause between queries

                r = session.get("https://gtbuses.herokuapp.com/agencies/georgia-tech/routes/" + route + "/predictions")
                r2 = session.get("https://gtbuses.herokuapp.com/agencies/georgia-tech/routes/" + route + "/vehicles")
                if r.status_code != 200 or r2.status_code != 200:
                    continue
                stops = xmltodict.parse(r.text)["body"]["predictions"]

                # All stops for this route
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
                    row.append(str(layover)) # Is this bus' prediction inacurrate?
                    row.append(str(is_departure)) # Is the bus waiting?
                    row.append(arrival_epoch) # Predicted timestamp of arrival
                    row.append(seconds_arrival) # Seconds to arrival prediction
                    row.append(weather_json["main"]["temp"]) # Temp in kelvin
                    row.append(weather_json["main"]["pressure"]) # Air pressure
                    row.append(weather_json["main"]["humidity"]) # Air humidity
                    row.append(weather_json["visibility"]) # Air visibility
                    row.append(weather_name) # cloudy, rainy, sunny...
                    row.append(weather_json["wind"]["speed"]) # Wind speed
                    row.append(weather_json["clouds"]["all"]) # Cloud coverage

                    # Use these features to predict actualSecondsToArrival
                    my_prediction = predict.predict(model, row)[0]
                    row.append(my_prediction
                    )
                    print(str(my_prediction) + " from " + str(seconds_arrival))
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
                    sql.query_write(query)

                    log.log("Inserted for " + route_name + " at " + stop_name)

        except Exception as e:
            log.log("Exception:")
            log.log(traceback.format_exc())

if __name__ == "__main__":
    run()
