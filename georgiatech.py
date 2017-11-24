import requests
import xmltodict
from collections import defaultdict

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
                    if not str(stop["@tag"]) in self.stop_names[str(stop["@title"])]:
                        self.stop_names[str(stop["@title"])].append(str(stop["@tag"]))
                    self.stop_coords[(route["@tag"], stop["@tag"])] = (float(stop["@lat"]), float(stop["@lon"]))
        except:
            print("You are offline - cannot load stop_coords")

    # CONSTANTS
    stop_coords = {} # Auto-populated
    stop_names = defaultdict(list) # Auto-populated
    all_routes = ["red", "blue", "green", "trolley", "night", "tech"]
    route_colors = {
        "red": "#FE1C00",
        "green": "#0FCB66",
        "blue": "#0F03FF",
        "tech": "#FFFF00",
        "trolley": "#CA8E20",
        "night": "#774BA7"
    }
    mw_class_schedule = [
        (480, 530),
        (545, 595),
        (610, 660),
        (675, 725),
        (740, 790),
        (835, 885),
        (900, 975),
        (990, 1065),
        (1080, 1155),
        (1170, 1245)
    ]
    tr_class_schedule = [
        (480, 555),
        (570, 645),
        (720, 795),
        (810, 885),
        (900, 975),
        (990, 1065),
        (1080, 1155),
        (1170, 1245)
    ]
    f_class_schedule = [
        (480, 530),
        (545, 595),
        (610, 660),
        (675, 725),
        (740, 790),
        (835, 885),
        (900, 1155)
    ]