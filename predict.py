import feature_engineering as fe
import pandas as pd
from georgiatech import GeorgiaTech
import cleaner

gt = GeorgiaTech()
header = ["timestamp", "stop", "route", "kmperhr", "busID", "numBuses", "busLat", "busLong", "layover", "isDeparture", "predictedArrival", "secondsToArrival", "temperature", "pressure", "humidity", "visibility", "weather", "wind", "cloudCoverage"]
stops = ['10thhemp', '14thbusy_a', '14thstat', '3rdtech', '4thtech', '5thtech', '5thtech_ib', '8thhemp', '8thwvil', 'bakebldg', 'centrstud', 'cherfers', 'cloucomm', 'creccent', 'creccent_ib', 'creccent_ob', 'duprmrt', 'fersatl_ib', 'fersatla', 'ferschmrt', 'ferschrec', 'fersfomrt', 'fersforec', 'fersfowl', 'fershemp', 'fershemp_ob', 'fershemrt', 'fersherec', 'fershub', 'fersklau', 'fersstat', 'fersstat_ob', 'ferstcher', 'ferstdr', 'fitthall', 'fitthall_a', 'gcat', 'glc', 'hempcurr', 'hubfers', 'klaubldg', 'marta_a', 'naveapts_a', 'ndec', 'publix', 'reccent', 'reccent_ob', 'recctr', 'studcent', 'studcent_ib', 'studcentr', 'tech4th', 'tech4th_ib', 'tech4th_ob', 'tech5mrt', 'tech5rec', 'tech5th', 'techbob', 'technorth', 'technorth_ib', 'technorth_ob', 'techsqua', 'techsqua_ib', 'techsqua_ob', 'tranhub', 'tranhub_a', 'tranhub_b', 'tranhub_f', 'wpe7mrt']
routes = ['blue', 'green', 'night', 'red', 'tech', 'trolley']
maxes = [5939.0, 90.369132314, 1.0, 1.0, 2.0, 1.0, 1.0, 1439.0, 29.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
mins = [0.0, 9.99999997475e-07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# Given a model, make a prediction for an instance.
# You need to update this class whenever the model changes structurally.
# This means if more features are added or your training set changes (and hence
# maxes/mins change)
# Current schema:
# 'secondsToArrival', 'distance', 'layover', 'isDeparture', 'classMode', 'morningRush', 'eveningRush', 'minutesIntoDay', 'kmperhr', 'is_10thhemp', 'is_14thbusy_a', 'is_14thstat', 'is_3rdtech', 'is_4thtech', 'is_5thtech', 'is_5thtech_ib', 'is_8thhemp', 'is_8thwvil', 'is_bakebldg', 'is_centrstud', 'is_cherfers', 'is_cloucomm', 'is_creccent', 'is_creccent_ib', 'is_creccent_ob', 'is_duprmrt', 'is_fersatl_ib', 'is_fersatla', 'is_ferschmrt', 'is_ferschrec', 'is_fersfomrt', 'is_fersforec', 'is_fersfowl', 'is_fershemp', 'is_fershemp_ob', 'is_fershemrt', 'is_fersherec', 'is_fershub', 'is_fersklau', 'is_fersstat', 'is_fersstat_ob', 'is_ferstcher', 'is_ferstdr', 'is_fitthall', 'is_fitthall_a', 'is_gcat', 'is_glc', 'is_hempcurr', 'is_hubfers', 'is_klaubldg', 'is_marta_a', 'is_naveapts_a', 'is_ndec', 'is_publix', 'is_reccent', 'is_reccent_ob', 'is_recctr', 'is_studcent', 'is_studcent_ib', 'is_studcentr', 'is_tech4th', 'is_tech4th_ib', 'is_tech4th_ob', 'is_tech5mrt', 'is_tech5rec', 'is_tech5th', 'is_techbob', 'is_technorth', 'is_technorth_ib', 'is_technorth_ob', 'is_techsqua', 'is_techsqua_ib', 'is_techsqua_ob', 'is_tranhub', 'is_tranhub_a', 'is_tranhub_b', 'is_tranhub_f', 'is_wpe7mrt', 'is_blue', 'is_green', 'is_night', 'is_red', 'is_tech', 'is_trolley', 'actualSecondsToArrival'
def predict(model, instance):
    maxes_np = pd.DataFrame(maxes).transpose()
    mins_np = pd.DataFrame(mins).transpose()
    copy = pd.DataFrame(instance).transpose()
    build = []
    copy.columns = header
    copy = fe.temporal(copy)
    copy = fe.georgiatech(copy, gt)
    build.append(copy.ix[0,"secondsToArrival"])
    build.append(float(copy.ix[0,"distance"]))
    build.append(float(copy.ix[0,"layover"] == True))
    build.append(float(copy.ix[0,"isDeparture"] == True))
    build.append(float(copy.ix[0,"classMode"]))
    build.append(float(copy.ix[0,"morningRush"]))
    build.append(float(copy.ix[0,"eveningRush"]))
    build.append(float(copy.ix[0,"minutesIntoDay"]))
    build.append(float(copy.ix[0,"kmperhr"]))
    for item in stops:
        build.append(1.0 if copy.ix[0,"stop"] == item else 0.0)
    for item in routes:
        build.append(1.0 if copy.ix[0,"route"] == item else 0.0)
    build = pd.DataFrame(build).transpose()
    temp = maxes_np - mins_np
    temp[temp == 0] = 1
    build -= mins_np
    build /= temp
    return model.predict([build])

if __name__ == "__main__":
    # Predict a dummy instance for testing
    from sklearn.externals import joblib
    model = joblib.load('model_bad.pkl') 
    instance = [1511633365, u'ferschmrt', u'trolley', u'0', u'404', 1, u'33.776981', u'-84.389058', 'True', 'False', 1511634755, 1390, 288.04, 1016, 41, 16093, u'Clear', 1.5, 1]
    print(predict(model, instance))