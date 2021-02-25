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

session=Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    print("server received a request for 'Home' page")
    return "Surfs Up!"



all_precipitation=[]
@app.route("/api/v1.0/precipitation")
def prcp():
    result_prcp=session.query(Measurement.date, Measurement.prcp).all()
    
    precpitation={}
    for x in result_prcp:
        precpitation["date"]= date
        precipitation["prcp"]= prcp
        all_precipitation.append(precipitation)
    return jsonify(all_precipitation)






if __name__=='__main__':
    app.run(debug=True)

