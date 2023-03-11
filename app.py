import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# print(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Base.classes.keys()
Measurement = Base.classes.measurement
#Station=Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"<h1>Welcome to the Climate API!</h1><br/>"
        f"<h2>Please choose the available Routes:<h2><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperature<br/>"
        f"/api/v1.0/<small>enter start date here</small><start><br/>"
        f"/api/v1.0/<small>enter start date here</small><start>/<small>enter end date here</small><end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    """The precipitation data is below"""
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    session.close()
    # Create a dictionary from the row data and append to a list of {date: prcp}
    prc=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    list_prc=[]
    for i in range(0, len(prc)):
        list_prc.append({prc[i][0]: prc[i][1]})

    return jsonify(list_prc)



@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    """The list of meteorological stations is below"""
    results = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station)).all()
    session.close()
    stations=list(np.ravel(results))
    
    return jsonify(stations)


@app.route("/api/v1.0/temperature")
def temperature():
    session = Session(engine)

    """The temperature data from the most-active station is below"""
    temp=session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date >= '2016-08-18').order_by(Measurement.date).all()
    list_temp=[]
    for i in range(0, len(temp)):
        list_temp.append({temp[i][0]: temp[i][1]})

    return jsonify(list_temp)


###########################################
###########################################


@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    #start=datetime.strptime(start,"%y-%m-%d")
    """The min, average and max temperatures from the selected date are below"""
    temp_min=session.query(func.min(Measurement.tobs)).filter(Measurement.station=='USC00519281').filter(Measurement.date >= start).all()
    temp_avg=session.query(func.avg(Measurement.tobs)).filter(Measurement.station=='USC00519281').filter(Measurement.date >= start).all()
    temp_max=session.query(func.max(Measurement.tobs)).filter(Measurement.station=='USC00519281').filter(Measurement.date >= start).all()
    
    session.close()
    # Create a dictionary from the results above
    temp_dic={}
    temp_dic['Temperature_min']=[x[0] for x in temp_min]
    temp_dic['Temperature_average']=[x[0] for x in temp_avg]
    temp_dic['Temperature_max']=[x[0] for x in temp_max]

    return jsonify(temp_dic)



@app.route("/api/v1.0/<start>/<end>")
def end_date(start, end):
    session = Session(engine)
    
    """The min, average and max temperatures from the selected time frame are below"""
    temp_min=session.query(Measurement.date, func.min(Measurement.tobs)).filter(Measurement.station=='USC00519281').filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp_avg=session.query(Measurement.date, func.avg(Measurement.tobs)).filter(Measurement.station=='USC00519281').filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp_max=session.query(Measurement.date, func.max(Measurement.tobs)).filter(Measurement.station=='USC00519281').filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
   # Create a dictionary from the results above
    temp_dic={}
    temp_dic['Temperature_min']=[x[0] for x in temp_min]
    temp_dic['Temperature_average']=[x[0] for x in temp_avg]
    temp_dic['Temperature_max']=[x[0] for x in temp_max]

    return jsonify(temp_dic)


if __name__ == "__main__":
    
    app.run(debug=True)
