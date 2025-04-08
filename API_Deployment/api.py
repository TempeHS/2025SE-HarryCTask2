from flask import Flask
from flask import request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from model_prediction import Model

# Add Auth Key

api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

Model = Model(model=None)
Model.load_model("A_MV_model_v8.sav")


#logging.basicConfig(
    #filename="api_security_log.log",
    #encoding="utf-8",
    #level=logging.DEBUG,
    #format="%(asctime)s %(message)s",
#)

@api.route("/get_prediction", methods=["GET","POST"])
@limiter.limit("3/second", override_defaults=False)
def post():
    data = request.get_json()
    response = Model.predict(data)
    return response, 200


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)