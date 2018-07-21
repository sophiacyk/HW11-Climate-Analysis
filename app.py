import datetime as dt
import numpy as np
import pandas as pd

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################


# 1. Homepage and available routes
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"<h1>Welcome! This is the home page for climate analysis.</h1><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )
 


# 2. Precipation for the last 12 months 
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the dates and precipitation observations from the last year."""
    # Query all passengers

    prcp_1yr = engine.execute("SELECT m.date, SUM(m.prcp) AS prcp \
    FROM measurement m \
    WHERE m.date BETWEEN \
    date((SELECT max(date) FROM measurement), '-12 months') AND (SELECT max(date) FROM measurement) \
    GROUP BY m.date \
    ORDER BY m.date").fetchall()

    all_prcp = []
    for prcp in prcp_1yr:
        prcp_dict = {}
        prcp_dict["date"] = prcp.date
        prcp_dict["precipitation"] = round(prcp.prcp, 2)
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

# 3. Stations
@app.route("/api/v1.0/stations")
def station():
    stations = session.query(Station).all()
    all_stations = []
    for station in stations:
        station_dict = {}
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


# 4. Tobs for the last 12 months  
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the dates and temperature observations from the last year."""
    # Query all passengers

    tobs_1yr = engine.execute("SELECT m.date, m.tobs\
                          FROM measurement m \
                          WHERE m.date BETWEEN \
                          date((SELECT max(date) FROM measurement), '-12 months') AND (SELECT max(date) FROM measurement) \
                          GROUP BY m.date \
                          ORDER BY m.date").fetchall()

    all_tobs = []
    for tobs in tobs_1yr:
        tobs_dict = {}
        tobs_dict["date"] = tobs.date
        tobs_dict["tobs"] = tobs.tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)





if __name__ == "__main__":
    app.run(debug=True)