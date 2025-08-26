from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # allow frontend requests

# Connect to MongoDB (same URI you used)
client = MongoClient("mongodb://localhost:27017/")  # ⚡ change if using Docker
db = client["holidaysdb"]
holidays_collection = db["holidays"]

# GET all holidays
@app.route("/holidays", methods=["GET"])
def get_holidays():
    holidays = list(holidays_collection.find({}, {"_id": 0}))
    return jsonify(holidays)

# POST new holiday
@app.route("/holidays", methods=["POST"])
def create_holiday():
    holiday_data = request.json
    holidays_collection.insert_one(holiday_data)
    holiday_data.pop("_id", None)  # remove ObjectId if exists
    return jsonify(holiday_data), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
