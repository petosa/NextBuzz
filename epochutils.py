import datetime
import pytz

# Returns the given epoch's hour clock time
def epoch_to_hour(e):
    return int(pytz.timezone("US/Eastern").localize(datetime.datetime.fromtimestamp(e)).strftime('%H'))

# Returns the given epoch's minute clock time
def epoch_to_minute(e):
    return int(pytz.timezone("US/Eastern").localize(datetime.datetime.fromtimestamp(e)).strftime('%M'))

# Returns the given epoch's day of week
def epoch_to_day_of_week(e):
    return pytz.timezone("US/Eastern").localize(datetime.datetime.fromtimestamp(e)).strftime('%A')

# Returns the given epoch's month as int
def epoch_to_month(e):
    return int(pytz.timezone("US/Eastern").localize(datetime.datetime.fromtimestamp(e)).strftime('%m'))

# Returns the given epoch's semester
def epoch_to_semester(e):
    month = epoch_to_month(e)
    if month >= 8:
        return "fall"
    if month >= 5:
        return "summer"
    return "spring"

def epoch_to_time_as_number(e):
    return int(pytz.timezone("US/Eastern").localize(datetime.datetime.fromtimestamp(e)).strftime('%H%M'))

def epoch_is_between_classes(e):
    dow = epoch_to_day_of_week(e)
    time = epoch_to_time_as_number(e)

    if (dow == "Monday" or dow == "Wednesday"):
        return (850 <= time and 905 >= time) or (955 <= time and 1010 >= time) or (1100 <= time and 1115 >= time) or (1205 <= time and 1220 >= time) or (1310 <= time and 1355 >= time) or (1445 <= time and 1500 >= time) or (1615 <= time and 1630 >= time) or (1745 <= time and 1800 >= time) or (1915 <= time and 1930 >= time)
    if(dow == "Friday"):
        return (850 <= time and 905 >= time) or (955 <= time and 1010 >= time) or (1100 <= time and 1115 >= time) or (1205 <= time and 1220 >= time) or (1310 <= time and 1355 >= time) or (1445 <= time and 1500 >= time)
    if(dow == "Tuesday" or dow == "Thursday"):
        return (915 <= time and 930 >= time) or (1045 <= time and 1200 >= time) or (1315 <= time and 1330 >= time) or (1445 <= time and 1500 >= time) or (1615 <= time and 1630 >= time) or (1745 <= time and 1800 >= time) or (1915 <= time and 1930 >= time)
    
    return False

def epoch_is_weekend(e):
    dow = epoch_to_day_of_week(e)
    return dow == "Saturday" or dow == "Sunday"

schedule_weekday = {
    "red": [
        [range(700, 1730), "red1"],
        [range(1730, 1845), "red2"],
        [range(1845, 2200), "red3"]
    ],
    "blue": [
        [range(700, 1730), "blue1"],
        [range(1730, 1845), "blue2"],
        [range(1845, 2200), "blue3"]
    ],
    "green": [
        [range(645, 750), "green1"],
        [range(750, 1750), "green2"],
        [range(1750, 2050), "green3"]
    ],
    "trolley": [
        [range(545, 620), "trolley1"],
        [range(620, 730), "trolley2"],
        [range(730, 1745), "trolley3"],
        [range(1745, 1845), "trolley4"],
        [range(1845, 1940), "trolley5"],
        [range(1940, 2230), "trolley6"]
    ]
}

def epoch_to_shift(e, route):
    if epoch_is_weekend(e):
        return "invalid"
    if not route in schedule_weekday:
        return "invalid"
    time = epoch_to_time_as_number(e)
    for item in schedule_weekday[route]:
        if time in item[0]:
            return item[1]
    return "invalid"
