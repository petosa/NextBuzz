import xmltodict
import requests
import time
import os
import epochutils

all_routes = ["red", "blue", "green", "trolley", "night", "tech"]

with open("predictions.csv", "a") as file:
    if os.stat("predictions.csv").st_size == 0:
        file.write("timestamp,stop,route,kmperhr,layover,isDeparture,predictedArrival,secondsToArrival,hour,timeAsInt,betweenClass,dayOfWeek,month,semester,shift,isWeekend,temperature,pressure,humidity,visibility,weather,wind,cloudCoverage\n")

while True:
    time.sleep(5)
    weather = requests.get("https://api.openweathermap.org/data/2.5/weather?q=atlanta&APPID=00c4c655fa601a48dc5bf4f34c4ce86a")

    if weather.status_code != 200:
        continue

    weather_json = weather.json()

    for route in all_routes:
        time.sleep(2)
        r = requests.get("https://gtbuses.herokuapp.com/agencies/georgia-tech/routes/" + route + "/predictions")
        r2 = requests.get("https://gtbuses.herokuapp.com/agencies/georgia-tech/routes/" + route + "/vehicles")

        if r.status_code != 200 or r2.status_code != 200:
            continue
        
        stops = xmltodict.parse(r.text)["body"]["predictions"]
        for stop in stops:
            stop_name = stop["@stopTag"]
            route_name = stop["@routeTag"]

            # First determine if there are any predictions
            if "direction" not in stop:
                print("No predictions for stop " + stop_name + " for route " + route_name)
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
            kmperhr = -1
            for v in vehicles:
                if bus_number == v["@id"]:
                    kmperhr = v["@speedKmHr"]

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
            row.append(layover) # Is this bus' prediction inacurrate?
            row.append(is_departure) # Is the bus waiting?
            row.append(arrival_epoch) # Predicted timestamp of arrival
            row.append(seconds_arrival) # Seconds to arrival prediction
            row.append(epochutils.epoch_to_hour(current_epoch)) # 0-23
            row.append(epochutils.epoch_to_time_as_number(current_epoch)) # 1:03 -> 103
            row.append(epochutils.epoch_is_between_classes(current_epoch)) # Time is in a class gap
            row.append(epochutils.epoch_to_day_of_week(current_epoch)) # Monday, Tuesday...
            row.append(epochutils.epoch_to_month(current_epoch)) # 1-12
            row.append(epochutils.epoch_to_semester(current_epoch)) # spring, summer, fall
            row.append(epochutils.epoch_to_shift(current_epoch, route_name)) # look up bus schedules
            row.append(epochutils.epoch_is_weekend(current_epoch)) # Sunday or Saturday?
            row.append(weather_json["main"]["temp"]) # Temp in kelvin
            row.append(weather_json["main"]["pressure"]) # Air pressure
            row.append(weather_json["main"]["humidity"]) # Air humidity
            row.append(weather_json["visibility"]) # Air visibility
            row.append(weather_name) # cloudy, rainy, sunny...
            row.append(weather_json["wind"]["speed"]) # Wind speed
            row.append(weather_json["clouds"]["all"]) # Cloud coverage

            with open("predictions.csv", "a") as file:
                file.write(str(row)[1:len(str(row))-1].replace(" ","").replace("\'","") + "\n")


            print("Logged for " + route_name + " at " + stop_name)      
