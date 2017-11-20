import requests
import xmltodict

class GeorgiaTech(object):

    def __init__(self):
        # Calculate stop_coords
        session = requests.Session()
        session.headers.update({"User-Agent": "NextBuzz (nick.petosa@gmail.com)"})
        try:
            response = session.get("https://gtbuses.herokuapp.com/agencies/georgia-tech/routes")
            routes = xmltodict.parse(response.text)["body"]["route"]
            self.stop_coords = {}
            for route in routes:
                for stop in route["stop"]:
                    self.stop_coords[(route["@tag"], stop["@tag"])] = ((float(route["@latMin"]) + float(route["@latMax"]))/2, (float(route["@lonMin"]) + float(route["@lonMax"]))/2)
            print("There are " + str(len(self.stop_coords.keys())) + " route/stop combinations at GT.")
        except:
            print("You are offline - cannot load stop_coords")

    # CONSTANTS
    stop_coords = {} # Auto-populated
    route_colors = {
        "red": "#FE1C00",
        "green": "#0FCB66",
        "blue": "#0F03FF",
        "tech": "#FFFF00",
        "trolley": "#CA8E20",
        "night": "#774BA7"
    }