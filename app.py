import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation values"""
    # Query all passengers
    results = session.query(Measurement.prcp, Measurement.date).all()

    session.close()

   # Create a dictionary from the row data and append to a list
    all_prcp = []
    for prcp, date in results:
        measurement_dict = {}
        measurement_dict["prcp"] = prcp
        measurement_dict["date"] = date
        all_prcp.append(measurement_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs in last year of data"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date > '2016-08-23').\
            order_by(Measurement.date).all()

    session.close()

   # Create a dictionary from the row data and append to a list
    all_tobs = []
    for tobs, date in results:
        measurement_dict = {}
        measurement_dict["tobs"] = tobs
        measurement_dict["date"] = date
        all_tobs.append(measurement_dict)

    return jsonify(all_tobs)






if __name__ == '__main__':
    app.run(debug=True)
