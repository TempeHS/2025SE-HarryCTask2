import bleach
from datetime import datetime
from flask import jsonify, request
from flask import Flask
from flask_cors import CORS
import requests
import sqlite3 as sql

def usr_input(request_form):
    # Extract data from the request form
    num_bed = request_form["num_bed"]
    num_bath = request_form["num_bath"]
    property_size = request_form["property_size"]
    suburb_median_income = request_form["suburb_median_income"]
    suburb = request_form["suburb"]
    date = request_form["date"]
    num_parking = request_form["num_parking"]
    save_to_db = "save_to_db" in request_form

    # Clean the input data
    num_bed = bleach.clean(num_bed)
    num_bath = bleach.clean(num_bath)
    property_size = bleach.clean(property_size)
    suburb_median_income = bleach.clean(suburb_median_income)
    suburb = bleach.clean(suburb)
    date = bleach.clean(date)
    num_parking = bleach.clean(num_parking)

    # Convert to correct data types
    num_bed = int(num_bed)
    num_bath = int(num_bath)
    property_size = float(property_size)
    suburb_median_income = float(suburb_median_income)
    suburb = str(suburb)
    date = str(date)
    num_parking = int(num_parking)

    # Validate data
    data = {
        "num_bed": num_bed,
        "num_bath": num_bath,
        "property_size": property_size,
        "suburb_median_income": suburb_median_income,
        "suburb": suburb,
        "date": date,
        "num_parking": num_parking,
        "save_to_db": save_to_db
    }

    return data

def add_db(data):
    try:
        conn = sql.connect(".databseFiles/database.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO property_data (
                num_bed, num_bath, property_size, value_score, tot_rooms,
                suburb_median_income, suburb_lat, suburb_lng, km_from_cbd,
                ds_float, num_parking
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["num_bed"],
            data["num_bath"],
            data["property_size"],
            data["value_score"],
            data["tot_rooms"],  
            data["suburb_median_income"],
            data["suburb_lat"],  
            data["suburb_lng"],  
            data["km_from_cbd"], 
            data["ds_float"],  
            data["num_parking"]
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False

def main():
    data = {
        "num_bed": 3,
        "num_bath": 2,
        "property_size": 120,
        "value_score": 0.8,
        "tot_rooms": 5,
        "suburb_median_income": 60000,
        "suburb_lat": -33.8708,
        "suburb_lng": 151.2073,
        "km_from_cbd": 0.5,
        "ds_float": 1601510400.0,
        "num_parking": 1
    }
    add_db(data)

if __name__ == "__main__":
    main()