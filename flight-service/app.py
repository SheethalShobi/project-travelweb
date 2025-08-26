from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://flight-mongo:27017/")
db = client.flightdb
flights = db.flights

@app.route('/flights', methods=['GET'])
def get_flights():
    return jsonify(list(flights.find({}, {'_id': 0})))

@app.route('/book', methods=['POST'])
def book_flight():
    data = request.json
    flights.insert_one(data)
    return jsonify({"message":"Flight booked successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True