from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/TechElevate"
mongo = PyMongo(app)

# Serve the single signin.html which contains both signin & signup forms
@app.route('/')
def index():
    return render_template('signin.html')

# Signup API
@app.route('/api/signin', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')

    if mongo.db.users.find_one({'email': email}):
        return jsonify({'status': 'fail', 'message': 'Email already registered.'}), 400

    hashed_password = generate_password_hash(data['password'])

    user_data = {
        'name': data.get('name'),
        'email': email,
        'password': hashed_password,
        'phone': data.get('phone'),
        'college': data.get('college'),
        'branch': data.get('branch')
    }

    mongo.db.users.insert_one(user_data)
    return jsonify({'status': 'success', 'message': 'User registered successfully.'})

# Login API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = mongo.db.users.find_one({'email': email})

    if user and check_password_hash(user['password'], password):
        return jsonify({'status': 'success', 'message': 'Login successful.'})
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid credentials.'}), 401

if __name__ == '__main__':
    app.run(debug=True)
