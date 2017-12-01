mae      0.172126
medae    0.260859
rmse     0.114699



dataset.csv

0-20k
mae      0.133261
medae    0.099732
rmse     0.106227

20k-40k
mae      0.080765
medae   -0.081400
rmse     0.118345

0-40k, 100 estimators
mae     -0.020205
medae   -0.129283
rmse    -0.014245

min_split_size {
-Split 50
mae     -0.037213
medae   -0.312342
rmse     0.017490
-Split 100
mae     -0.016510
medae   -0.306533
rmse     0.050852
-Split 200
mae     -0.031677
medae   -0.310952
rmse     0.034808
}

features {
+dayOfWeek
mae     -0.018364
medae   -0.137587
rmse    -0.010391
secondsToArrival
mae      0.055420
medae    0.038286
rmse    -0.004819
secondsToArrival,dayOfWeek
mae      0.057374
medae    0.040263
rmse    -0.000548
secondsToArrival,dayOfWeek,distance
mae      0.082552
medae    0.070000
rmse     0.021599
secondsToArrival,dayOfWeek,distance,kmperhr
mae      0.083497
medae    0.082867
rmse     0.022859
secondsToArrival,dayOfWeek,distance,kmperhr,layover
mae      0.089138
medae    0.076085
rmse     0.027700
secondsToArrival,dayOfWeek,distance,kmperhr,isDeparture
mae      0.084397
medae    0.076595
rmse     0.023037
secondsToArrival,dayOfWeek,distance,kmperhr,minutesIntoDay
mae     -0.023848
medae   -0.137276
rmse    -0.016921
secondsToArrival,dayOfWeek,distance,kmperhr,morningRush
mae      0.083323
medae    0.081004
rmse     0.022183
secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush
mae      0.083579
medae    0.083530
rmse     0.022230
secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush,classMode
mae      0.067118
medae    0.121400
rmse    -0.022389

}
secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush
0-80k, 100 estimators
mae      0.101692
medae    0.126955
rmse    -0.050491

features {
secondsToArrival,distance,kmperhr,eveningRush
mae      0.100174
medae    0.127609
rmse    -0.053185
secondsToArrival
mae      0.056229
medae    0.068296
rmse    -0.078331
secondsToArrival,distance,kmperhr,eveningRush,minutesToArrival
mae     -0.053728
medae    0.026467
rmse    -0.176538

}

min_split_size {
Split 500

}

0-160k, 10 estimators
secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush
mae     -0.077095
medae   -0.079785
rmse    -0.107362


max_samples {
.5
mae     -0.046839
medae   -0.046308
rmse    -0.083215
.2, 10 estimators
mae     -0.029311
medae   -0.073548
rmse    -0.043360
.2, 100 estimators
mae      0.003441
medae   -0.008232
rmse    -0.018493
.2, 100 estimators, secondsToArrival
mae      0.017358
medae    0.036310
rmse    -0.052024
.1, 100 estimators,
mae      0.016274
medae   -0.020065
rmse     0.006333
.1, 200 estimators,
mae      0.021364
medae   -0.012769
rmse     0.008458
.1, 300 estimators,
mae      0.017417
medae   -0.019952
rmse     0.004956
1000 samples, 200 estimators
mae      0.038959
medae   -0.068108
rmse     0.056215
1000 samples, 400 estimators
mae      0.043670
medae   -0.069599
rmse     0.062818
1000 samples, 400 estimators, secondsToArrival
mae      0.065604
medae   -0.006086
rmse     0.066491
1000 samples, 400 estimators, secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush,humidity
mae      0.029310
medae   -0.079118
rmse     0.057459
1000 samples, 400 estimators, secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush,pressure
mae      0.082159
medae   -0.007263
rmse     0.092297
1000 samples, 400 estimators, secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush,pressure,morningRush
mae      0.076753
medae   -0.016124
rmse     0.087606
1000 samples, 400 estimators, secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush,pressure,wind
mae      0.059045
medae   -0.075495
rmse     0.097079
1000 samples, 400 estimators, secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush,pressure,temperature
mae      0.023381
medae   -0.103153
rmse     0.066732
1000 samples, 400 estimators, secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush,pressure,visibility
mae      0.079883
medae   -0.013952
rmse     0.090120
1000 samples, 400 estimators, secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush,pressure,busID
mae      0.069503
medae   -0.022790
rmse     0.084391


}

0-320k, 1000 samples, 400 estimators, 1000 samples, 400 estimators, secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush
mae      0.110417
medae   -0.026820
rmse     0.076320

{
2000 samples, 400 estimators
mae      0.11708564142
medae   -0.02419871794
rmse     0.10517122712
4000 samples, 400 estimators
mae      0.11832
medae   -0.016257
rmse     0.108568
8000 samples, 400 estimators
mae      0.113122
medae   -0.015214
rmse     0.109644

All
(max_samples=3000, n_estimators=400)
secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush
{'mae': 182.19415500110929, 'medae': 101.33000000000001, 'rmse': 367.9542994493536}
secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush,pressure
{196, 115, 392}
secondsToArrival,dayOfWeek,distance,kmperhr,eveningRush,minutesIntoDay
Bad
secondsToArrival,dayOfWeek,distance,kmperhr,minutesIntoDay
{'mae': 178.40064775117685, 'medae': 95.638749999999987, 'rmse': 363.08774338811565}
secondsToArrival,distance,kmperhr,minutesIntoDay
{'mae': 167.943284856394, 'medae': 86.048749999999984, 'rmse': 358.8260266481942}
secondsToArrival,distance,kmperhr,minutesIntoDay,layover
{'mae': 167.31292921174591, 'medae': 85.783749999999998, 'rmse': 358.3976251490235}


(max_samples=3000, n_estimators=75)
secondsToArrival,distance,kmperhr,minutesIntoDay
{177,89,386}
secondsToArrival,distance,minutesIntoDay,layover
{'mae': 168.65406469070786, 'medae': 87.146666666666647, 'rmse': 358.28333669961796}
secondsToArrival,kmperhr,minutesIntoDay,layover
Bad
secondsToArrival,distance,minutesIntoDay,layover,isDeparture
Bad
secondsToArrival,distance,minutesIntoDay,layover,classMode
Bad

(max_samples=1000, n_estimators=75)
secondsToArrival,distance,minutesIntoDay,layover
{'mae': 170.78765390115021, 'medae': 88.74666666666667, 'rmse': 365.5547240992596}

(max_samples=5000, n_estimators=75)
secondsToArrival,distance,minutesIntoDay,layover
{'mae': 166.7952535371152, 'medae': 84.333333333333371, 'rmse': 356.5755381620684}

(max_samples=10000, n_estimators=75)
{'mae': 165.90029892004023, 'medae': 83.360000000000014, 'rmse': 354.0919949619977}

(max_samples=32000, n_estimators=75)
{'mae': 163.17913550318505, 'medae': 79.399999999999977, 'rmse': 347.7779449628575}

(max_samples=50000, n_estimators=75)
{'mae': 163.1159747707103, 'medae': 77.806666666666729, 'rmse': 349.56821118414155}

(max_samples=50000, n_estimators=150)
{'mae': 161.93836866535068, 'medae': 77.25333333333333, 'rmse': 347.41317199015197}
