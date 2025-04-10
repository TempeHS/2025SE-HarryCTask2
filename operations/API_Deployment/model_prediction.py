import pickle
import numpy as np
from flask import jsonify
import sqlite3 as sql
from jsonschema import validate
from flask import current_app
from datetime import datetime
import json
import requests
from haversine import haversine

schema = {
    "type": "object",
    "validationLevel": "strict",
    "required": [
        "num_bed",
        "num_bath",
        "property_size",
        "suburb_median_income",
        "suburb",
        "date",
        "num_parking",
        "save_to_db"
    ],
    "properties": {
        "num_bed": {
            "type": "integer",
        },
        "num_bath": {
            "type": "integer",
        },
        "property_size": {
            "type": "number",
        },
        "suburb_median_income": {
            "type": "number",
        },
        "suburb": {
            "type": "string",
        },
        "date": {
            "type": "string",
        },
        "num_parking": {
            "type": "integer",
        },
        "save_to_db": {
            "type": "boolean",
        }
    },
    "additionalProperties": False,
}

class Model:
    def __init__(self, model):
        self.model = model

    def load_model(self, model_path):
        try:
            with open(model_path, "rb") as file:
                self.model = pickle.load(file)
            return self.model
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e
    
    def scale_property_size(self, property_size):
        # Scale property size to a range of 0 to 1 (The same way that was done in feature engineering)
        # For scaling you could use dataframe min and max values by importing the pandas library, though this way was more efficient
        min_size = 40
        max_size = 1270
        scaled_size = (property_size - min_size) / (max_size - min_size)
        return scaled_size
    
    def value_score(self, scaled_size, scaled_km):
        value_score = scaled_size * np.exp(-scaled_km)
        return value_score

    def tot_rooms(self, num_bed, num_bath):
        tot_rooms = num_bed + num_bath
        return tot_rooms
    
    def ds_float(self, date):
        date = datetime.strptime(date, "%Y-%m-%d")
        ds_float = date.timestamp()
        return ds_float
    
    def get_suburb_lat(self, suburb):
        # Useing OPEN CAGE API to get the suburb latitude
        api_key = "6dd7914425ca470d8f76a158ff4fb4d5"
        url = f"https://api.opencagedata.com/geocode/v1/json?q={suburb}, Australia&key={api_key}"

        response = requests.get(url)
        data = response.json()

        if data['results']:
            coords = data['results'][0]['geometry']
            return coords['lat']
        
    def get_suburb_lng(self, suburb):
        # Useing OPEN CAGE API to get the suburb latitude
        api_key = "6dd7914425ca470d8f76a158ff4fb4d5"
        url = f"https://api.opencagedata.com/geocode/v1/json?q={suburb}, Australia&key={api_key}"

        response = requests.get(url)
        data = response.json()

        if data['results']:
            coords = data['results'][0]['geometry']
            return coords['lng']
    
    def scale_km_from_cbd(self, suburb_lat, suburb_lng):
        # Using Haversine libarary to calculate distance in km between coordinates
        # For scaling you could use dataframe min and max values by importing the pandas library, though this way was more efficient
        cbd_coords = (-33.8708, 151.2073)
        suburb_coords = (suburb_lat, suburb_lng)
        km_from_cbd = haversine(cbd_coords, suburb_coords, unit='km')
        # Scale km_from_cbd to a range of 0 to 1
        min_km = 0.3
        max_km = 82
        scaled_km = (km_from_cbd - min_km) / (max_km - min_km)
        return scaled_km
    
    def process_data(self, data):
        try:
            # Validate the input data against the schema
            validate(instance=data, schema=schema)

            # Process all the required features
            data["property_size"] = self.scale_property_size(data["property_size"])
            # The original database had oddly low values for suburb median income, that looked half of what they should be, though based off my obersvations, I decided to half the suburb median income
            data["suburb_median_income"] = data["suburb_median_income"] / 2
            data["tot_rooms"] = self.tot_rooms(data["num_bed"], data["num_bath"])
            data["suburb_lat"] = self.get_suburb_lat(data["suburb"])
            data["suburb_lng"] = self.get_suburb_lng(data["suburb"])
            data["ds_float"] = self.ds_float(data["date"])
            del data["date"] 
            data["km_from_cbd"] = self.scale_km_from_cbd(data["suburb_lat"], data["suburb_lng"])
            data["value_score"] = self.value_score(data["property_size"], data["km_from_cbd"])

            # Log the processed data
            mx_col = ["num_bed", "num_bath", "property_size", "value_score", "tot_rooms", "suburb_median_income", "suburb_lat", "suburb_lng", "km_from_cbd", "ds_float", "num_parking"]
            ordered_data = {col: data[col] for col in mx_col if col in data} # Reorder the data to match the model's input, without this it changes the order
            return ordered_data
        except Exception as e:
            print(f"Error during data processing: {e}")
            return {"error": str(e)}, 400

    def predict(self, data):
        try:
            data = self.process_data(data)
            # Convert the processed data to a numpy array
            features = np.array(list(data.values())).reshape(1, -1)
            # Make prediction
            prediction = self.model.predict(features)
            # Formats prediction so it can be passed onto the front end
            formatted_prediction = f"${int(round(prediction[0])):,}"
            return jsonify({"prediction": formatted_prediction}) # Not using JSNOIFY as it was causing issues with the front end 
        except Exception as e:
            print(f"Error during prediction: {e}")
            return {"error": str(e)}, 500