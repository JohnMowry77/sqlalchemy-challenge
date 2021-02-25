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
Measurement=Base.classes.measurement
Station=Base.classes.station
#create session (link) from Python to the DB
session=Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Home Page
# List all routes that are available
@app.route("/")
def home():
    print("server received a request for 'Home' page")
    return (f"Surfs Up!"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs"
            f"/api/v1.0/<start>/<end>"
            )

#convert  query results to a dict using 'date' as the key & 'prcp' as the value

#create a dict from the row data and append to a list all_precipitation
#note you were asked to convert the dict to a json, no list needed. 
all_precipitation=[]
@app.route("/api/v1.0/precipitation")
def prcp():
    result_prcp=session.query(Measurement.date, Measurement.prcp).all()
    
    precpitation={}
    for date,prcp in result_prcp:
        precpitation["date"]= date
        precpitation["prcp"]= prcp
        all_precipitation.append(precpitation)
        #precpitation[date]=prcp
    return jsonify(all_precipitation)
    #return jsonify(result_prep)

#Return the JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    result_station=session.query(Station.station).all()
    #session.close()
    #convert list of tuples into normal lsit
    all_stations= list(np.ravel(result_station))
    return jsonify(all_stations)

#Query the dates & temprature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    sel=[Measurement.station, Measurement.date, Measurement.tobs]
    results=session.query(*sel).filter(Measurement.date>=2017,8,23)\
    .filter(Measurement.station==most_active_station).all()

    most_active=[]
    for station, date, tobs in results:
        most_active_station={}
        most_active_station["station"]= station
        most_active_station["date"]= date
        most_active_station["tobs"]= tobs
        most_active.append(most_active_station)

@




if __name__=='__main__':
    app.run(debug=True)