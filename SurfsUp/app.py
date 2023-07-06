# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
    
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

Base.prepare(engine, reflect = True)

# reflect the tables
classes = Base.classes
classes_name = Base.classes.keys()
print(classes_name)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    """Homepage."""
    return (
        f"Welcome to the Hawaii Climate API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation data for the last 12 months<br/>"
        f"/api/v1.0/stations - List of stations<br/>"
        f"/api/v1.0/tobs - Temperature observations for the last 12 months<br/>"
        f"/api/v1.0/&lt;start&gt; - Min, Avg, and Max temperatures from a start date (format: 'yyyy-mm-dd')<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt; - Min, Avg, and Max temperatures within a date range (format: 'yyyy-mm-dd')<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    """Return the JSON representation of the last 12 months of precipitation data."""
    # Calculate the date one year ago from the most recent date in the database
    one_year_ago = dt.date.today() - dt.timedelta(days=365)

    # Perform the query to retrieve the last 12 months of precipitation data
    results = session.query(measurement.date, measurement.prcp).\
              filter(measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    """Return a JSON list of stations from the dataset."""
    # Perform the query to retrieve all stations
    results = session.query(station.station, station.name).all()

    # Convert the query results to a list of dictionaries
    station_list = []
    for station, name in results:
        station_list.append({
            'station': station,
            'name': name
        })

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    """Return a JSON list of temperature observations for the previous year for the most active station."""
    # Calculate the date one year ago from the most recent date in the database
    one_year_ago = dt.date.today() - dt.timedelta(days=365)

    # Perform the query to retrieve the temperature observations for the most active station
    results = session.query(measurement.date, measurement.tobs).\
              filter(measurement.station == 'USC00519281').\
              filter(measurement.date >= one_year_ago).all()


    
    