# Step 2 - Climate App

#Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

#* Use Flask to create your routes.

#Libraries

import numpy as np 
import pandas as Pd 
import datetime as dt

#Other tools

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#data

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect = True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


### Routes


@app.route("/")
def home():
    return (
        f"Welcome! I LOVE flask!<br/>"
        f"These are the available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"      
    )


 # * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

 # * Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.datetime(2017,8,23) - dt.timedelta(days = 365)
    prcp_result = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).all()
    precipitation = {date:prcp for date, prcp in prcp_result}
    return jsonify(precipitation)


#  * Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
#    stationsq = session.query(station.name, station.station)
#    station_list = pd.read_sql(stationsq.statement, stationsq.session.bind)
#    return jsonify(station_list.to_dict())
#    station_result
    station_result = session.query(station.station).all()
    station_list = list(np.ravel(station_result))
    return jsonify(station_list)

#Query the dates and temperature observations of the most active station for the last year of data.
#from previous excercise, we know latest date is 23/08/2017 and most active station USC00519281

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.datetime(2017,8,23) - dt.timedelta(days = 365)
    tobs_result = session.query(measurement.date,measurement.tobs).filter(measurement.station== "USC00519281").filter(measurement.date >= last_year).all()
    
    temp_date = []

    for tob  in tobs_result:
        row = {}
        row["date"] = tobs_result[0] 
        row["tobs"] = tobs_result[1]
        temp_date.append(row)
    
    #tobs_list = list(np.ravel(tobs_result))
    return jsonify(temp_date)


    # * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

 # * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  #* When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

app.route("/api/v1.0/<start>")
def starting(start):

    temp_query = session.query(func.min(measurement.tobs),func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    temps = []

    for minT, maxT, avgT in temp_query: 
        dict = {}
        dict['Min_temp']=minT
        dict['Max_temp']=maxT
        dict['Avg_temp']=avgT
        temps.append(dict)

    return jsonify(temps)


 #   temps= list(np.ravel(temp_query))
#unsuccssful approach
    #return jsonify(temps)
#for temp in temp_query: 
#    dict = {}
#    dict['date']=temp[0]
#    dict['Min_temp']=temp[1]
#    dict['Max_temp']=temp[3]
#    dict['Avg_temp']=temp[2]
#    list.append(dict)




@app.route("/api/v1.0/<start>/<end>")
def starting_ending(start,end):

    temp_query = session.query(func.min(measurement.tobs),func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()

  

    temps = []

    for minT, maxT, avgT in temp_query: 
        dict = {}
        dict['Min_temp']=minT
        dict['Max_temp']=maxT
        dict['Avg_temp']=avgT
        temps.append(dict)

    return jsonify(temps)


if __name__ == '__main__':
    #url = 'http://127.0.0.1:5000/'
    #webbrowser.open_new(url)
    app.run(debug=True)