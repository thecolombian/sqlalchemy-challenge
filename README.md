# Weather Data Analysis Project

## Overview
This project is designed to analyze weather data using SQLite, SQLAlchemy, Pandas, Matplotlib, and Flask. The project consists of two main parts: a Jupyter Notebook for data analysis and a Flask API to serve the analysis results.

## Requirements
The project is divided into several tasks, each with specific requirements:

1. **Jupyter Notebook Database Connection **
2. **Precipitation Analysis **
3. **Station Analysis**
4. **API SQLite Connection & Landing Page**
5. **API Static Routes **
6. **API Dynamic Route **

### Jupyter Notebook Database Connection
- Use `SQLAlchemy create_engine()` to connect to the SQLite database.
- Use `SQLAlchemy automap_base()` to reflect tables into classes.
- Save references to the classes named `station` and `measurement`.
- Link Python to the database by creating a SQLAlchemy session.
- Close the session at the end of the notebook.

### Precipitation Analysis
- Create a query that finds the most recent date in the dataset (`8/23/2017`).
- Create a query to collect data and precipitation for the last year of data.
- Save the query results to a Pandas DataFrame with date and precipitation columns.
- Sort the DataFrame by date.
- Plot the results using the DataFrame `plot` method.
- Print summary statistics for the precipitation data using Pandas.

### Station Analysis
- Design a query to find the number of stations in the dataset.
- Design a query to list stations and observation counts in descending order and find the most active station (`USC00519281`).
- Design a query to find the most active station's minimum, max, and average temperatures.
- Design a query to get the previous 12 months of temperature observation data filtered by the station with the most observations.
- Save the query results to a Pandas DataFrame.
- Plot a histogram with `bins=12` for the last year of data using `tobs` as the column to count.

### API SQLite Connection & Landing Page
To achieve full points:
- Correctly generate the engine to the SQLite file.
- Use `automap_base()` and reflect the database schema.
- Correctly save references to the tables in the SQLite file (`measurement` and `station`).
- Correctly create and bind the session between the Python app and database.
- Display the available routes on the landing page.

### API Static Routes
- A precipitation route that:
  - Returns JSON with the date as the key and precipitation as the value.
  - Only returns precipitation data for the last year in the database.
- A stations route that:
  - Returns JSON data of all stations in the database.
- A `tobs` route that:
  - Returns JSON data for the most active station (`USC00519281`).
  - Only returns data for the last year.

### API Dynamic Route
- A start route that:
  - Accepts the start date as a URL parameter.
  - Returns min, max, and average temperatures from the given start date to the end of the dataset.
- A start/end route that:
  - Accepts the start and end dates as URL parameters.
  - Returns min, max, and average temperatures from the given start to the end date.

