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
#################################################S

@app.route('/')
def home():
    """Homepage."""
    return (
        f"Welcome to the Hawaii Climate API!<br/><br/>"
        f"Here you can find out available Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation data for the last 12 months<br/>"
        f"/api/v1.0/stations - List of stations<br/>"
        f"/api/v1.0/tobs - Temperature observations for the last 12 months of the most-active station<br/>"
        f"/api/v1.0/2015-01-23 - Min, Avg, and Max temperatures from a start date (try 2015-01-23)<br/>"
        f"/api/v1.0/2015-01-26/2017-01-01 - Min, Avg, and Max temperatures within a date range (try 2015-01-26/2017-01-01)<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    """Return the JSON representation of the last 12 months of precipitation data."""
    # Calculate the date one year ago from the most recent date in the database
    most_recent_date = dt.date(2017, 8, 23)
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Create a new session and perform the query to retrieve the last 12 months of precipitation data
    with Session(engine) as session:
        results = session.query(measurement.date, measurement.prcp).\
                  filter(measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    """Return a JSON list of stations from the dataset."""
    # Create a new session and perform the query to retrieve all stations
    with Session(engine) as session:
        results = session.query(station.station, station.name).all()

    # Convert the query results to a list of dictionaries
    station_list = []
    for row in results:
        station_list.append({
            'station': row.station,
            'name': row.name
        })

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    """Return a JSON list of temperature observations for the previous year for the most active station."""
    # Calculate the date one year ago from the most recent date in the database (2017-08-23)
    most_recent_date = dt.date(2017, 8, 23)
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Find the most active station
    with Session(engine) as session:
        most_active_station = session.query(measurement.station).\
                              group_by(measurement.station).\
                              order_by(func.count(measurement.station).desc()).\
                              first()[0]

    # Create a new session and perform the query to retrieve the temperature observations for the most active station within the last year
    with Session(engine) as session:
        results = session.query(measurement.date, measurement.tobs).\
                  filter(measurement.station == most_active_station).\
                  filter(measurement.date >= one_year_ago).all()

    # Convert the query results to a list of dictionaries
    tobs_list = []
    for date, tobs in results:
        tobs_list.append({
            'date': date,
            'tobs': tobs
        })

    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def temp_stats_start(start):
    """Return a JSON list of TMIN, TAVG, and TMAX for all dates greater than or equal to the start date."""
    # Create a new session and perform the query to calculate TMIN, TAVG, and TMAX for the dates greater than or equal to the start date
    with Session(engine) as session:
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                  filter(measurement.date >= start).all()

    # Convert the query results to a list of dictionaries
    temp_stats_list = []
    for Tmin, Tavg, Tmax in results:
        temp_stats_list.append({
            'TMIN': Tmin,
            'TAVG': Tavg,
            'TMAX': Tmax
        })

    return jsonify(temp_stats_list)

@app.route('/api/v1.0/<start>/<end>')
def temp_stats_range(start, end):
    """Return a JSON list of TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""
    # Create a new session and perform the query to calculate TMIN, TAVG, and TMAX for the dates within the specified range
    with Session(engine) as session:
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                  filter(measurement.date >= start).filter(measurement.date <= end).all()

    # Convert the query results to a list of dictionaries
    temp_stats_list = []
    for Tmin, Tavg, Tmax in results:
        temp_stats_list.append({
            'TMIN': Tmin,
            'TAVG': Tavg,
            'TMAX': Tmax
        })

    return jsonify(temp_stats_list)

if __name__ == "__main__":
    app.run(debug=True)
