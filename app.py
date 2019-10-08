### Routes
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)



@app.route("/")
def home():
    return (
        f"Availible Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/(start_date)<br/>"
        f"/api/v1.0/(start_date)/(end_date)<br/>"
        f"Date format: yyyy-dd-mm, end date optional")

@app.route("/api/v1.0/precipitation")
def precipitation():
  session = Session(engine)
  results = session.query(Measurement.date, Measurement.prcp)
  session.close()

  all_prcp = []
  for date, prcp in results:
    prcp_dict = {}
    prcp_dict["date"] = date
    prcp_dict["prcp"] = prcp
    all_prcp.append(prcp_dict)
  return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
  session = Session(engine)
  results = session.query(Station.station, Station.name)
  session.close()

  all_stations = []
  for station, name in results:
    station_dict = {}
    station_dict["name"] = station
    station_dict["station"] = name
    all_stations.append(station_dict)
  return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
  session = Session(engine)
  results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date> '2016-08-23')
  session.close()
  all_tobs = []
  for date, tobs in results:
    result_tobs = {}
    result_tobs["date"] = date
    result_tobs["Temps"] = tobs
    all_tobs.append(result_tobs)
  return jsonify(all_tobs)

datey = ""
@app.route("/api/v1.0/<date_input>")
def weather(date_input):
  session = Session(engine)
  results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > date_input)
  session.close()
  your_weather = []
  for date, tobs in results:
    weathers = {}
    weathers["date"] = date
    weathers["temp"] = tobs
    your_weather.append(weathers)
  return jsonify(your_weather)

@app.route("/api/v1.0/<date_input>/<end_date>")
def weather2(date_input, end_date):
  session = Session(engine)
  results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date_input).filter(Measurement.date <= end_date).all()
  session.close()
  your_weather = []
  for min, avg, max in results:
    weathers = {}
    weathers["minimum temp"] = min
    weathers["average temp"] = avg
    weathers["maximum temp"] = max
    your_weather.append(weathers)
  return jsonify(your_weather)


  return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)

"""

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

## Hints

* You will need to join the station and measurement tables for some of the analysis queries.

* Use Flask `jsonify` to convert your API data into a valid JSON response object.

- - -"""