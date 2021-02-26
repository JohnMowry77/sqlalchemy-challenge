import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

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
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
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
    # measurement_count=session.query(Measurement.station,func.count(Measurement.date))\
    # .group_by(Measurement.station)\
    # .order_by(func.count(Measurement.date).desc()).all()

    most_active_station = "USC00519281"
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    sel=[Measurement.station, Measurement.date, Measurement.tobs]
    results=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year ).\
    filter(Measurement.station==most_active_station).all()

    #print(results)
    # most_active=[]
    # for station, date, tobs in results:
    #     most_active_stations={}
    #     most_active_stations["station"]= station
    #     most_active_stations["date"]= date
    #     most_active_stations["tobs"]= tobs
    #     most_active.append(most_active_stations)
    most_active = list(np.ravel(results))
    return jsonify(most_active)
    
#Return a JSON list of the min temp, avg temp, max temp for a given start or start-end range.
#When given the start only, calculate 'TMIN', 'TAVG', & 'TMAX' for all dates >= to the start date.


@app.route("/api/v1.0/<start>")
def start():
 #Date input format = 8-5-17 ISO
    start_date=datetime.strptime(start, "%Y-%m-%d").date()

    temp_calc= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    results_temp= list(np.ravel(temp_calc))

    min_temp= results_temp[0]
    avg_temp= results_temp[1]
    max_temp= results_temp[2]

    temp_data=[]
    #Create a list of dictionaries & append to empty list temp_data
    temp_dict= [{"Start Date": start_date},\
    {"The minimum temperature for this date was": min_temp},\
    {"The average temperature for this date was": avg_temp},\
    {"The maximum temperature for this date was": max_temp}]
    temp_data.append(temp_dict)

    return jsonify(temp_data)

    session.close()
#When given the start & the end date, calculate the 'TMIN', 'TAVG', & 'TMAX' for dates between the start & end date inclusive.

#  temp_calc= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

if __name__=='__main__':
    app.run(debug=True)