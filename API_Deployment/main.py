from flask import Flask
from flask import request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from model_prediction import Model
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from flask import jsonify
from jsonschema import validate
from flask import current_app
from flask import session
import json
from flask import make_response
from flask import render_template
import requests
import form as form


app = Flask(__name__)



@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        data = form.usr_input(request.form)
        response = requests.post(
            "http://127.0.0.1:3000/get_prediction",
            json=data,
        )
        if response.status_code == 200:
            prediction = response.json()
            # Save the prediction to the database if requested (Ask Sir if we are to include predicted score)
            if data["save_to_db"]:
                form.add_db(data)
            return render_template("index.html", success=True, prediction=prediction)
        else:
            return render_template("index.html", error=True)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)