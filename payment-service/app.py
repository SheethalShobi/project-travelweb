from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('payments.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS payments
(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, amount REAL, status TEXT)''')
conn.commit()

@app.route('/payment', methods=['POST'])
def payment():
    data = request.json
    cursor.execute("INSERT INTO payments (user_id, amount, status) VALUES (?,?,?)",
                   (data['user_id'], data['amount'], 'success'))
    conn.commit()
    return jsonify({"message":"Payment successful"}), 201

@app.route('/payment/<int:user_id>', methods=['GET'])
def get_payments(user_id):
    cursor.execute("SELECT * FROM payments WHERE user_id=?", (user_id,))
    payments = cursor.fetchall()
    return jsonify([{"id":p[0],"user_id":p[1],"amount":p[2],"status":p[3]} for p in payments])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)