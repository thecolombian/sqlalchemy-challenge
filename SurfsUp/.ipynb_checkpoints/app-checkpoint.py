import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create an engine to connect to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the existing database into a new model
Base = automap_base()
# Reflect the tables in the database using autoload_with parameter
Base.prepare(autoload_with=engine)

# Save references to each table in the database
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

# Initialize a Flask application
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        """
        <html>
            <head>
                <title>SQL-Alchemy APP API</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; }
                    .container { margin: 0 auto; max-width: 600px; padding: 20px; }
                    h1 { color: #333; }
                    ul { list-style-type: none; padding: 0; }
                    li { margin: 10px 0; }
                    a { text-decoration: none; color: #1e90ff; }
                    a:hover { text-decoration: underline; }
                    form { margin-top: 10px; }
                    input[type="text"] { padding: 5px; margin-right: 10px; }
                    input[type="submit"] { padding: 5px 10px; }
                </style>
                <script>
                    function navigateToStart() {
                        const startDate = document.getElementById('start_date').value;
                        window.location.href = `/api/v1.0/${startDate}`;
                    }

                    function navigateToStartEnd() {
                        const startDate = document.getElementById('start_date_range').value;
                        const endDate = document.getElementById('end_date').value;
                        window.location.href = `/api/v1.0/${startDate}.${endDate}`;
                    }
                </script>
            </head>
            <body>
                <div class="container">
                    <h1>Welcome to the SQL-Alchemy APP API!</h1>
                    <p>Available Routes:</p>
                    <ul>
                        <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a> <br> Returns JSON with the date as the key and the value as the precipitation. Only returns the JSONified precipitation data for the last year in the database.</li>
                        <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>  Stations route that returns jsonified data of all of the stations in the database.</li>
                        <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li> tobs route:
                        Returns jsonified data for the most active station (USC00519281)
                        Only returns the jsonified data for the last year of data.</li>
                        .....................................................................................................................................................</li>
                        <li>
                        Accepts the start date as a parameter from the URL </li>
                            /api/v1.0/[start_date format: yyyy-mm-dd]
                            <form onsubmit="navigateToStart(); return false;">
                                <input type="text" id="start_date" placeholder="Example: 2016-11-09" />
                                <input type="submit" value="Go" />
                            </form>
                        </li>
                        <li>
                        Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset </li>
                            /api/v1.0/[start_date format: yyyy-mm-dd]/[end_date format: yyyy-mm-dd]
                            <form onsubmit="navigateToStartEnd(); return false;">
                            
                                <input type="text" id="start_date_range" placeholder="Example: 2016-11-09" />
                                <input type="text" id="end_date" placeholder="Example: 2016-11-16" />
                                <input type="submit" value="Go" />
                            </form>
                        </li>
                    </ul>
                </div>
            </body>
        </html>
        """
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all Precipitation Data"""
    
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation data from the Measurement table
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()

    # Close the session
    session.close()
    
    # Convert the query results to a dictionary with date as the key and prcp as the value
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all Stations"""
    
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Query all station data from the Station table
    results = session.query(Station.station).order_by(Station.station).all()

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    # Return the JSON representation of the list
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations (TOBs) for the last year of data"""
    
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Query temperature observations from the Measurement table for the last year of data
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station == 'USC00519281').\
                order_by(Measurement.date).all()

    # Close the session
    session.close()

    # Convert the query results to a list of dictionaries
    all_tobs = []
    for date, tobs, prcp in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_dict["prcp"] = prcp
        all_tobs.append(tobs_dict)

    # Return the JSON representation of the list
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    """Return a list of min, avg, and max temperature observations (TOBs) from a given start date"""
    
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Query minimum, average, and maximum temperatures from the Measurement table for the given start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    # Close the session
    session.close()

    # Convert the query results to a list of dictionaries
    start_date_tobs = []
    for min_temp, avg_temp, max_temp in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min_temp
        start_date_tobs_dict["avg_temp"] = avg_temp
        start_date_tobs_dict["max_temp"] = max_temp
        start_date_tobs.append(start_date_tobs_dict)

    # Return the JSON representation of the list
    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    """Return a list of min, avg, and max temperature observations (TOBs) for a given date range"""
    
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Query minimum, average, and maximum temperatures from the Measurement table for the given date range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).\
                filter(Measurement.date <= end_date).all()

    # Close the session
    session.close()

    # Convert the query results to a list of dictionaries
    start_end_tobs = []
    for min_temp, avg_temp, max_temp in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min_temp
        start_end_tobs_dict["avg_temp"] = avg_temp
        start_end_tobs_dict["max_temp"] = max_temp
        start_end_tobs.append(start_end_tobs_dict)

    # Return the JSON representation of the list
    return jsonify(start_end_tobs)

if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
