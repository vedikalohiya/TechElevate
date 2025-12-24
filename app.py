import os
import re
from flask import Flask, render_template, request, jsonify, session, send_from_directory, abort, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from flask_cors import CORS
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
CORS(app)

# Session configuration with security
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# MongoDB configuration - use environment variable
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/techelevate')
mongo = PyMongo(app)

# uploads folder for ATS uploads
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# local ATS ranker module
try:
    import ai_ranker as ar
except Exception as e:
    ar = None
    print(f"Warning: ai_ranker module not available: {e}")


# === AUTHENTICATION DECORATOR ===
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('sign_in'))
        return f(*args, **kwargs)
    return decorated_function

def subscription_required(tier='free'):
    """Check if user has required subscription tier"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('sign_in'))
            
            user = mongo.db.users.find_one({'_id': session['user_id']})
            if not user:
                return redirect(url_for('sign_in'))
            
            tier_hierarchy = {'free': 0, 'basic': 1, 'pro': 2, 'premium': 3}
            user_tier = user.get('subscription_tier', 'free')
            
            if tier_hierarchy.get(user_tier, 0) < tier_hierarchy.get(tier, 0):
                return redirect(url_for('pricing'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


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
@login_required
def show_profile():
    user = mongo.db.users.find_one({'_id': session['user_id']})
    return render_template('profile.html', user=user)

@app.route('/dashboard')
@login_required
def show_dashboard():
    user = mongo.db.users.find_one({'_id': session['user_id']})
    return render_template('dash.html', user=user)

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


# === USER AUTHENTICATION ===
@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Validation
        if not email or not password or not name:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        if len(password) < 8:
            return jsonify({'success': False, 'message': 'Password must be at least 8 characters'}), 400
        
        if len(name) < 2 or len(name) > 100:
            return jsonify({'success': False, 'message': 'Name must be between 2 and 100 characters'}), 400
        
        # Check if user exists
        if mongo.db.users.find_one({'email': email}):
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Create user
        user_id = email  # Use email as ID
        hashed_password = generate_password_hash(password)
        
        user_data = {
            '_id': user_id,
            'email': email,
            'name': name,
            'password': hashed_password,
            'subscription_tier': 'free',
            'subscription_status': 'active',
            'subscription_start': datetime.utcnow(),
            'subscription_end': None,
            'resumes_created': 0,
            'job_matches_used': 0,
            'cover_letters_generated': 0,
            'created_at': datetime.utcnow(),
            'last_login': datetime.utcnow()
        }
        
        mongo.db.users.insert_one(user_data)
        
        # Set session
        session['user_id'] = user_id
        session['user_name'] = name
        session['subscription_tier'] = 'free'
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'redirect': '/dashboard'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        # Find user
        user = mongo.db.users.find_one({'email': email})
        
        if not user or not check_password_hash(user['password'], password):
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Update last login
        mongo.db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'last_login': datetime.utcnow()}}
        )
        
        # Set session
        session['user_id'] = user['_id']
        session['user_name'] = user['name']
        session['subscription_tier'] = user.get('subscription_tier', 'free')
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'redirect': '/dashboard'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/logout')
def logout_user():
    session.clear()
    return redirect(url_for('home'))


@app.route('/api/user/profile', methods=['GET'])
@login_required
def get_user_profile():
    try:
        user = mongo.db.users.find_one({'_id': session['user_id']})
        if user:
            user.pop('password', None)  # Remove password from response
            user['_id'] = str(user['_id'])
            return jsonify({'success': True, 'user': user})
        return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/user/update', methods=['POST'])
@login_required
def update_user_profile():
    try:
        data = request.get_json()
        update_data = {}
        
        if 'name' in data:
            name = data['name'].strip()
            if len(name) < 2 or len(name) > 100:
                return jsonify({'success': False, 'message': 'Name must be between 2 and 100 characters'}), 400
            update_data['name'] = name
            session['user_name'] = update_data['name']
        
        if update_data:
            mongo.db.users.update_one(
                {'_id': session['user_id']},
                {'$set': update_data}
            )
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        
        return jsonify({'success': False, 'message': 'No data to update'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# === SUBSCRIPTION & PRICING ===
@app.route('/pricing')
def pricing():
    user_data = None
    if 'user_id' in session:
        user_data = mongo.db.users.find_one({'_id': session['user_id']})
    return render_template('pricing.html', user=user_data)


@app.route('/api/subscription/upgrade', methods=['POST'])
@login_required
def upgrade_subscription():
    try:
        data = request.get_json()
        tier = data.get('tier', '').lower()
        
        valid_tiers = ['basic', 'pro', 'premium']
        if tier not in valid_tiers:
            return jsonify({'success': False, 'message': 'Invalid subscription tier'}), 400
        
        # In production, integrate with Stripe/PayPal here
        # For now, simulate successful payment
        
        subscription_end = datetime.utcnow() + timedelta(days=30)  # 1 month
        
        mongo.db.users.update_one(
            {'_id': session['user_id']},
            {'$set': {
                'subscription_tier': tier,
                'subscription_status': 'active',
                'subscription_start': datetime.utcnow(),
                'subscription_end': subscription_end
            }}
        )
        
        session['subscription_tier'] = tier
        
        return jsonify({
            'success': True,
            'message': f'Successfully upgraded to {tier.capitalize()} plan',
            'tier': tier
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/subscription/cancel', methods=['POST'])
@login_required
def cancel_subscription():
    try:
        mongo.db.users.update_one(
            {'_id': session['user_id']},
            {'$set': {
                'subscription_tier': 'free',
                'subscription_status': 'cancelled',
                'subscription_end': datetime.utcnow()
            }}
        )
        
        session['subscription_tier'] = 'free'
        
        return jsonify({
            'success': True,
            'message': 'Subscription cancelled successfully'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# === USAGE TRACKING ===
@app.route('/api/track/resume', methods=['POST'])
@login_required
def track_resume_creation():
    try:
        user = mongo.db.users.find_one({'_id': session['user_id']})
        tier = user.get('subscription_tier', 'free')
        count = user.get('resumes_created', 0)
        
        limits = {'free': 3, 'basic': 10, 'pro': 50, 'premium': 999999}
        
        if count >= limits.get(tier, 3):
            return jsonify({
                'success': False,
                'message': f'Resume limit reached. Upgrade to create more resumes.',
                'limit_reached': True
            }), 403
        
        mongo.db.users.update_one(
            {'_id': session['user_id']},
            {'$inc': {'resumes_created': 1}}
        )
        
        return jsonify({'success': True, 'count': count + 1})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/track/job-match', methods=['POST'])
@login_required
def track_job_match():
    try:
        user = mongo.db.users.find_one({'_id': session['user_id']})
        tier = user.get('subscription_tier', 'free')
        count = user.get('job_matches_used', 0)
        
        limits = {'free': 5, 'basic': 25, 'pro': 100, 'premium': 999999}
        
        if count >= limits.get(tier, 5):
            return jsonify({
                'success': False,
                'message': f'Job match limit reached. Upgrade for more analyses.',
                'limit_reached': True
            }), 403
        
        mongo.db.users.update_one(
            {'_id': session['user_id']},
            {'$inc': {'job_matches_used': 1}}
        )
        
        return jsonify({'success': True, 'count': count + 1})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/track/cover-letter', methods=['POST'])
@login_required
def track_cover_letter():
    try:
        user = mongo.db.users.find_one({'_id': session['user_id']})
        tier = user.get('subscription_tier', 'free')
        count = user.get('cover_letters_generated', 0)
        
        limits = {'free': 3, 'basic': 15, 'pro': 75, 'premium': 999999}
        
        if count >= limits.get(tier, 3):
            return jsonify({
                'success': False,
                'message': f'Cover letter limit reached. Upgrade for more generations.',
                'limit_reached': True
            }), 403
        
        mongo.db.users.update_one(
            {'_id': session['user_id']},
            {'$inc': {'cover_letters_generated': 1}}
        )
        
        return jsonify({'success': True, 'count': count + 1})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500



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


# Debug routes - only enable in development
if os.environ.get('FLASK_ENV') == 'development':
    @app.route('/__debug_template')
    def debug_template():
        tpl_rel = os.path.join('templates', 'softskills', 'softskills.html')
        tpl_path = os.path.abspath(tpl_rel)
        if not os.path.exists(tpl_path):
            return jsonify({'exists': False, 'path': tpl_path}), 404
        mtime = os.path.getmtime(tpl_path)
        with open(tpl_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return ('Path: ' + tpl_path + '\nModified: ' + str(mtime) + '\n\n' + content), 200, {'Content-Type': 'text/plain; charset=utf-8'}

    @app.route('/resume-debug')
    def resume_debug():
        return jsonify({'status': 'ok', 'message': 'resume debug route active'}), 200

    @app.route('/__routes')
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({'endpoint': rule.endpoint, 'rule': str(rule), 'methods': list(rule.methods)})
        return jsonify({'routes': routes}), 200


    @app.route('/__runtime')
    def runtime_info():
        try:
            import sys
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
    if request.method == 'GET':
        return render_template('ats_upload.html')

    # POST: process the uploaded resume file
    job_title = request.form.get('job_role', 'Unknown')
    job_desc = request.form.get('job_description', '')
    
    if not job_desc:
        return jsonify({'error': 'Job description is required'}), 400
    
    job_keywords = ar.extract_keywords_spacy(job_desc) if ar else []

    file = request.files.get('resume')
    if not file or not file.filename:
        return jsonify({'error': 'No file uploaded'}), 400

    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PDF, JPG, PNG, DOC, DOCX'}), 400

    filename = secure_filename(file.filename)
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    save_name = f"{ts}_{filename}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], save_name)
    
    try:
        file.save(path)
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

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

