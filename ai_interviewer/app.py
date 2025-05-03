from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from flask_pymongo import PyMongo
import re
import openai

app = Flask(__name__)
app.secret_key = ""

# MongoDB Config
app.config["MONGO_URI"] = "mongodb://localhost:27017/your_db_name"
mongo = PyMongo(app)

# OpenAI Config
openai.api_key = ""  # Replace with your actual OpenAI API key

# Route: Home page with AI Interviewer
@app.route('/')
def index():
    return render_template('index.html')

# Route: Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        confirm_email = request.form['confirm_email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        phone = request.form['phone']
        college = request.form['college']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format", "error")
            return redirect(url_for('register'))

        if email != confirm_email:
            flash("Emails do not match", "error")
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for('register'))

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            flash("Password must be at least 8 characters long with uppercase, lowercase, number, and special character.", "error")
            return redirect(url_for('register'))

        if not re.match(r"^[0-9]{10}$", phone):
            flash("Phone number must be exactly 10 digits", "error")
            return redirect(url_for('register'))

        # Save to MongoDB
        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": password,  # NOTE: Hash this in real apps!
            "phone": phone,
            "college": college
        })
        flash("Registration successful!", "success")
        return redirect(url_for('register'))

    return render_template('register.html')

# Route: AI Interviewer Chat Endpoint
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('message')
    prompt = f"You are an AI interviewer. Evaluate or respond to this candidate answer: \"{user_input}\". Be professional and constructive."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional AI interviewer."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        reply = "Sorry, an error occurred while processing your response."

    return jsonify({"reply": reply})


if __name__ == '__main__':
    app.run(debug=True)
