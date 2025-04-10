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
import model_prediction as model

app = Flask(__name__)
csrf = CSRFProtect(app)
app_header = {"Authorisation": "4L50v92nOgcDCYUM"}
app.secret_key = b"_53oi3uriq9pifpff;apl"

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            data = form.usr_input(request.form)
            response = requests.post(
                "http://127.0.0.1:3000/get_prediction",
                json=data, headers=app_header
            )
            # Check if the response is valid
            if response.status_code == 200:
                prediction = response.json()
                predicted_score = prediction["prediction"]
                data["predicted_score"] = predicted_score
                # Save the prediction to the database if requested
                if data["save_to_db"]:
                    form.add_db(data)
                return render_template("index.html", success=True, prediction=prediction)
        except ValueError as e:
            return render_template("index.html", error=True, message=f"{e}")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)