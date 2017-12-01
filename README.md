# NextBuzz
Using machine learning to predict Georgia Tech bus arrival times

## Overview
The purpose of this guide is to instruct you how do use all code that ships with NextBuzz, from exploratory analysis to
modeling to running the web app. For design documentation and project motivation, check out documentation/NextBuzz Proposal.pdf
and documentation/NextBuzz Final Report.pdf.

## Setting up the environment
This project was built with python 2.7. Making this project compatable with python 3.6 should not be that difficult, and is on
the roadmap.
### Installing necessary libraries
It is recommended that you install all python libraries in a virtual environment so as not to mess with your global pip
list. More information and virtualenv installation instructions can be found here: https://virtualenv.pypa.io/en/stable/

Once virtualenv is installed, you can create a new virtualenv in NextBuzz's repository doing something like `virtualenv nbenv`
followed by `source nbenv/bin/activate`. Once you have entered the virtual environment, it is safe to intall all required
packages. Do this with `pip install -r requirements.txt`. You may have to use `sudo` if that command fails.

## Collecting Data
One of the central features of NextBuzz is its data collection script, which will query NextBus and OpenWeatherMap for
updates every 20 seconds. If you do not yet have a model created, you can run `python collect.py False` to scrape data to
a database.db file without making a NextBuzz prediction. If you do have a model, make sure `model.pkl` is located in the same
directory as `collect.py` and run `python collect.py`.

## Preparing Data
Once you have collected data, export the section of the raw data that you want to clean as a CSV. From here, you can
load it into `pipeline.py` (looks in `data/rawdata.csv` by default) which will remove duplicates, turn strings into one-hot encodings, and engineer new features
related to arrival detection, time, and Georgia Tech domain knowledge. The output file will be `dataset.csv`.

## Exploratory Data Analysis
In `explore.py`, the `dataset.csv` you just created is loaded in. Assuming you have matplotlib installed, the script will then plot several features against the class to search for any correlations.

## Creating a Model
In `train.py`, the `dataset.csv` you just created is loaded in. From here, define the learner you want to apply to your data
using scikit-learn's API, and pass that learner in a call to either `supervised.rolling_kfold` for cross-validated error analysis,
and then `supervised.train_test_split` with high training percentage to generate a production-ready model. Pickle this model
to disk.

## Starting the Web App
In the root directory of the NextBus, run `python collect.py` to begin scraping real-time data to the database. 
Then call `cd webserver` and then `sh theServerIsDown.sh` to start the web server. Navigate to `http://0.0.0.0:8000/` in
you favorite browser to see the web app.

