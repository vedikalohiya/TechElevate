import os
from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/techelevate"
mongo = PyMongo(app)


# === HOME & PAGES ===
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile')
def show_profile():
    return render_template('profile.html', user_name="Guest")  # No login required

@app.route('/dashboard')
def show_dashboard():
    return render_template('dash.html', user_name="Guest")

@app.route('/mockstart')
def start_mock():
    return render_template('mockstart.html')

@app.route('/roadmap')
def show_roadmap():
    return render_template('roadmap.html')

@app.route('/skillset')
def show_skillset():
    return render_template('skillset.html')

@app.route('/technical')
def show_technical():
    return render_template('technical.html')

@app.route('/mock')
def show_mock():
    return render_template('mock.html')

@app.route('/aboutus')
def show_aboutus():
    return render_template('aboutus.html')

@app.route('/contact')
def show_contact():
    return render_template('contact.html')

@app.route('/settings')
def show_settings():
    return render_template('settings.html')

@app.route('/apti')
def show_apti():
    return render_template('apti.html')

@app.route('/technicals')
def show_technicals():
    return render_template('technical/technicals.html')

@app.route('/softskills')
def show_softskills():
    return render_template('softskills/softskills.html')

@app.route('/quantitative')
def show_quantitative():
    return render_template('aptitude/quantitative.html')

@app.route('/data-interpretation')
def show_data_interpretation():
    return render_template('aptitude/data-interpretation.html')

@app.route('/logical-reasoning')
def show_logical_reasoning():
    return render_template('aptitude/logical-reasoning.html')

@app.route('/time-and-work')
def show_time_and_work():
    return render_template('aptitude/time-and-work.html')

@app.route('/profit-and-loss')
def show_profit_and_loss():
    return render_template('aptitude/profit-and-loss.html')

@app.route('/speed-distance')
def show_speed_distance():
    return render_template('aptitude/speed-distance.html')

@app.route('/probability')
def show_probability():
    return render_template('aptitude/probability.html')

@app.route('/cpp')
def show_cpp():
    return render_template('technical/c++.html')

@app.route('/python')
def show_python():
    return render_template('technical/python.html')

@app.route('/java')
def show_java():
    return render_template('technical/java.html')

@app.route('/webdevelopment')
def show_webdev():
    return render_template('technical/webdevelopment.html')

@app.route('/webdevquiz')
def show_webdevquiz():
    return render_template('technical/webdevquiz.html')

@app.route('/html')
def show_html():
    return render_template('technical/html.html')

@app.route('/css')
def show_css():
    return render_template('technical/css.html')

@app.route('/js')
def show_js():
    return render_template('technical/js.html')


# === RUN APP ===
if __name__ == '__main__':
    app.run(debug=False)
