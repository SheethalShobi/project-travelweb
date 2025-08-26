from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password TEXT)''')
conn.commit()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    cursor.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
                   (data['name'], data['email'], data['password']))
    conn.commit()
    return jsonify({"message":"User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?",
                   (data['email'], data['password']))
    user = cursor.fetchone()
    if user:
        return jsonify({"id": user[0], "name": user[1], "email": user[2]})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/profile/<int:id>', methods=['GET'])
def profile(id):
    cursor.execute("SELECT id,name,email FROM users WHERE id=?", (id,))
    user = cursor.fetchone()
    if user:
        return jsonify({"id": user[0], "name": user[1], "email": user[2]})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)