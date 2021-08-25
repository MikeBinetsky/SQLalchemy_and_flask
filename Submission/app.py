## First I import my dependencies
import numpy as np

## VS studio claims this sqlalchemy import isn't used. Just the first one. Not sure why that is, pretty weird.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_
import datetime as dt

from flask import Flask, app, jsonify

## Create my engine
## This part is identical to the start of my

## Set up the engine
databasePath = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{databasePath}")

## set up the automap
Base = automap_base()
Base.prepare(engine, reflect = True)

## Set up my table classes
MeasurementTable = Base.classes.measurement
StationTable = Base.classes.station


##--------------------------------##
## Now I set up my flask & routes ##
##--------------------------------##

## Establishing Flask
app = Flask(__name__)

## Setting up the base route
@app.route("/")
def welcome():
    ## Create session link
    session = Session(engine)

    ## Close out session link
    session.close()

## Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    ## Create session link
    session = Session(engine)

    "Return a list of dates and precipitations in the data"
    results = session.query(MeasurementTable.date, MeasurementTable.prcp).all()

    ## Close out session link
    session.close()

    ## Now I can't use pandas here like I did on the starter code, so I think the best bet to make a dictionary to return would be a for loop.
    ## This is weird, to get this to work I have to set up a list of dictionaries so that the date is the index
    ## First I establish my list.
    precipList = []
    for date, prcp in results:
        ## Now I define an empty dictionary
        precipDict = {}
        precipDict["Date"] = date
        precipDict["Precipitation"] = prcp
        precipList.append(precipDict)

    ## Finally, I return the final list of dictionaries as a JSON
    return jsonify(precipList)


## Stations route
@app.route("/api/v1.0/stations")
def stations():
    ## Create session link
    session = Session(engine)

    "Returns a list of all stations in the data"
    results = session.query(StationTable.station).all()

    ## Close out session link
    session.close()

    ## I thought at first I should just get the station name, but instead I'm going to get the whole station details.
    ## Using the same details as the precipitation
    stationList = []
    for station, name, latitude, longitude, elevation in results:
        stationDict = {}
        stationDict["Station"] = station
        stationDict["Name"] = name
        stationDict["Latitude"] = latitude
        stationDict["Longitude"] = longitude
        stationDict["Elevation"] = elevation
        stationList.append(stationDict)

    return jsonify(stationList)

## Tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    ## Create session link

    ## This is a lot of code taken right from my notebook. Should work!
    session = Session(engine)

    stationActivity =  session.query(MeasurementTable.station, func.count(MeasurementTable.date)).\
    group_by(MeasurementTable.station).order_by(func.count(MeasurementTable.date).desc()).all()

    mostActive = stationActivity[0][0]

    oneYearPrior = dt.date(2017,8,23) - dt.timedelta(days=365)

    "Return a list of the last year of temperature data"
    results = session.query(MeasurementTable.date, MeasurementTable.tobs).filter(and_(MeasurementTable.date >= \
                oneYearPrior, MeasurementTable.station == mostActive)).all()

    ## Close out session link
    session.close()

    ## Another for loop to get the dictionary
    tobsList = []
    for date, tobs in results:
        tobsDict = {}
        tobsDict["Date"] = date
        tobsDict["Temperature"] = tobs
        tobsList.append(tobsDict)

    return jsonify(tobsList)

@app.route("/api/v1.0/<start>")
def startOnly():
    session = Session(engine)

    ## I should have used this method in the notebook. It's so much easier!

    results = session.query(func.min(MeasurementTable.tobs), func.max(MeasurementTable.tobs), func.avg(MeasurementTable.tobs)).\
        filter(MeasurementTable.tobs >= start).all()

    session.close()

    ## I think we can do ther same thing here
    justStartList = []
    for date, tobs in results:
        justStartDict = {}
        justStartDict["Date"] = date
        justStartDict["Temperature"] = tobs
        justStartList.append(justStartDict)

    return jsonify(justStartList)

@app.route('/api/v1.0/<start>/<end>')
def startAndEnd():

    session = Session(engine)

    ## I should have used this method in the notebook. It's so much easier!

    results = session.query(func.min(MeasurementTable.tobs), func.max(MeasurementTable.tobs), func.avg(MeasurementTable.tobs)).\
        filter(and_(MeasurementTable.tobs >= start, MeasurementTable.tobs <= end).all())

    session.close()

    ## I think we can do ther same thing here
    startEndList = []
    for date, tobs in results:
        startEndDict = {}
        startEndDict["Date"] = date
        startEndDict["Temperature"] = tobs
        startEndList.append(startEndDict)

    return jsonify(startEndList)