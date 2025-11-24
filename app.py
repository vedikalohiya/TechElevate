import os
import re
from flask import Flask, render_template, request, jsonify, session, send_from_directory, abort, redirect, url_for
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# simple session secret (use env var in production)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

app.config["MONGO_URI"] = "mongodb://localhost:27017/techelevate"
mongo = PyMongo(app)

# uploads folder for ATS uploads
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# local ATS ranker module
try:
    import ai_ranker as ar
except Exception:
    ar = None


# === HOME & PAGES ===
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/sign')
def sign_in():
    return render_template('sign.html')

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

@app.route('/resume-builder')
@app.route('/resume_builder')
def resume_builder():
    return render_template('resume_builder.html')

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


# === SOFTSKILLS SAVE / LOAD API ===
@app.route('/api/softskills', methods=['GET'])
def get_softskills():
    # try session first, then query param
    email = session.get('user_email') or request.args.get('email')
    if not email:
        return jsonify({'status': 'fail', 'message': 'Email required (login or pass ?email=)'}), 400
    doc = mongo.db.softskills.find_one({'email': email})
    if not doc:
        return jsonify({'status': 'success', 'data': {}}), 200
    doc.pop('_id', None)
    return jsonify({'status': 'success', 'data': doc}), 200


@app.route('/api/softskills', methods=['POST'])
def post_softskills():
    data = request.get_json() or {}
    email = session.get('user_email') or data.get('email')
    if not email:
        return jsonify({'status': 'fail', 'message': 'Email required to save.'}), 400
    save_doc = {
        'email': email,
        'habits': data.get('habits', {}),
        'role_play_answer': data.get('role_play_answer', ''),
        'updated_at': datetime.utcnow()
    }
    mongo.db.softskills.update_one({'email': email}, {'$set': save_doc}, upsert=True)
    return jsonify({'status': 'success', 'message': 'Softskills data saved.'}), 200


# Temporary debug route to verify which template file the server will serve
@app.route('/__debug_template')
def debug_template():
    # resolve template path and return file contents + mtime so we can confirm
    tpl_rel = os.path.join('templates', 'softskills', 'softskills.html')
    tpl_path = os.path.abspath(tpl_rel)
    if not os.path.exists(tpl_path):
        return jsonify({'exists': False, 'path': tpl_path}), 404
    mtime = os.path.getmtime(tpl_path)
    with open(tpl_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return ('Path: ' + tpl_path + '\nModified: ' + str(mtime) + '\n\n' + content), 200, {'Content-Type': 'text/plain; charset=utf-8'}


# Lightweight runtime debug endpoints
@app.route('/resume-debug')
def resume_debug():
    return jsonify({'status': 'ok', 'message': 'resume debug route active'}), 200

@app.route('/__routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({'endpoint': rule.endpoint, 'rule': str(rule), 'methods': list(rule.methods)})
    return jsonify({'routes': routes}), 200


# Runtime info endpoint to help debug which file/process is running
@app.route('/__runtime')
def runtime_info():
    try:
        import sys, os
        info = {
            'app_file': __file__,
            'app_root': app.root_path,
            'cwd': os.getcwd(),
            'python_executable': sys.executable,
            'pid': os.getpid()
        }
        return jsonify({'status': 'ok', 'runtime': info}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500


# Serve an embedded project directory if it's cloned into the workspace
@app.route('/embed/<path:subpath>', methods=['GET'])
def embed_project(subpath=''):
    base = os.path.join(app.root_path, 'ai_resume_ranker')
    if not os.path.isdir(base):
        return jsonify({'status': 'missing', 'message': 'ai_resume_ranker folder not found on server. Please git clone the project into the application root.'}), 404
    # normalize request: if a directory requested, serve its index.html
    requested_path = os.path.join(base, subpath)
    if os.path.isdir(requested_path):
        # ensure trailing index
        subpath = os.path.join(subpath, 'index.html') if subpath else 'index.html'
    try:
        return send_from_directory(base, subpath)
    except Exception:
        abort(404)


@app.route('/embed-check')
def embed_check():
    base = os.path.join(app.root_path, 'ai_resume_ranker')
    return jsonify({'exists': os.path.isdir(base), 'path': base}), 200


# --- ATS uploader and ranker routes ---
@app.route('/ats-upload', methods=['GET', 'POST'])
def ats_upload():
    # simple admin guard (reuse existing session admin flag)
    if request.method == 'GET':
        return render_template('ats_upload.html')

    # POST: process the uploaded resume file
    job_title = request.form.get('job_role', 'Unknown')
    job_desc = request.form.get('job_description', '')
    job_keywords = ar.extract_keywords_spacy(job_desc) if ar else []

    file = request.files.get('resume')
    if not file or not file.filename:
        return redirect(url_for('ats_upload'))

    filename = secure_filename(file.filename)
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    save_name = f"{ts}_{filename}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], save_name)
    file.save(path)

    # extract text
    text = ''
    if ar:
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            text = ar.extract_text_from_image(path)
        else:
            text = ar.extract_text_from_pdf_path(path)
    else:
        # fallback: read raw bytes as text
        try:
            with open(path, 'rb') as f:
                data = f.read()
                text = str(data[:2000])
        except Exception:
            text = ''

    text = re.sub(r"\s+", " ", (text or '').strip())

    # score
    if ar:
        score, matched_skills, tag, missing = ar.weighted_resume_score(text, set(job_keywords), job_desc)
    else:
        score, matched_skills, tag, missing = 0.0, [], 'Unknown', []

    results = [{
        'filename': filename,
        'score': score,
        'tag': tag,
        'matched_skills': matched_skills,
        'missing_skills': missing
    }]

    return render_template('ats_results.html', results=results, job_title=job_title, job_keywords=job_keywords)


# === RUN APP ===
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

