import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# setup database
engine = create_engine("sqlite:///../hawaii.sqlite", echo = False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#set up flask
app = Flask(__name__)

#create flask routes

@app.route("/")
def welcome():
    """List all available api routes."""
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#flask route and display for precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    mostrecent_date = dt.date(2017, 8 ,23)
    year_ago = mostrecent_date - dt.timedelta(days=365)

    past_temp = (session.query(Measurement.date, Measurement.prcp)
                .filter(Measurement.date <= maxDate)
                .filter(Measurement.date >= year_ago)
                .order_by(Measurement.date).all())
    
    precip = {date: prcp for date, prcp in past_temp}
    
    return jsonify(precip)

#flask route and display for stations

@app.route('/api/v1.0/stations')
def stations():

    avail_stations = session.query(Station.station).all()

    return jsonify(avail_stations)

#flask route and display for tobs

@app.route('/api/v1.0/tobs') 
def tobs():  
    mostrecent_date = dt.date(2017, 8 ,23)
    year_ago = mostrecent_date - dt.timedelta(days=365)

    lastyear = (session.query(Measurement.tobs)
                .filter(Measurement.station == 'USC00519281')
                .filter(Measurement.date <= mostrecent_date)
                .filter(Measurement.date >= year_ago)
                .order_by(Measurement.tobs).all())
    
    return jsonify(lastyear)

#starting point

@app.route('/api/v1.0/<start>') 
def start(start=None):

    #start = Measurement.date <= '2010-01-01'
    #end = Measurement.date >= '2017-08-23'

    normals = (session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017-08-23')).all())
    
    normals_df = pd.DataFrame(normals)

    tavg = normals_df["tobs"].mean()
    tmax = normals_df["tobs"].max()
    tmin = normals_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)

#start and end point

@app.route('/api/v1.0/<start>/<end>') 
def startend(start=None, end=None):

    #start = Measurement.date <= '2010-01-01'
    #end = Measurement.date >= '2017-08-23'

    normals = (session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all())
    
    normals_df = pd.DataFrame(normals)

    tavg = normals_df["tobs"].mean()
    tmax = normals_df["tobs"].max()
    tmin = normals_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)


if __name__ == '__main__':
    app.run(debug=True)