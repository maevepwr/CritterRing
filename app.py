from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm  # Import the forms
from models import db, User  # Import db and User model
import os
import json
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect


# Load the JSON data from the file
with open('critterring.json', 'r') as f:
    config = json.load(f)

# Accessing the values with capitalized Python variable names
RING_NAME = config['RING_NAME']
RING_ID = config['RING_ID']
RING_SITES = config['RING_SITES']
RING_INDEX = config['RING_INDEX']

app = Flask(__name__)
csrf = CSRFProtect(app)
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.cache = None
CORS(app)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "mysql+aiomysql://user:password@localhost:3306/your_database")

STATIC_FOLDER = os.path.join('static')


# Initialize the database
db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return "Welcome to the Flask App! <a href='/dashboard'>Dashboard</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')

            next_url = request.args.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(url_for('dashboard'))

        flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password_confirmation = form.password_confirmation.data
        
        # Create new user and hash the password
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! <a href="/logout">Logout</a>'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/critterring-widget.html')
def critterring_widget():
    login_form = LoginForm()


    context = {
        "ringName": RING_NAME,
        "ringID": RING_ID,
        "ringIndex": RING_INDEX,
        "loginForm": login_form,
        #"nextSite": next_site,
        #"prevSite": prev_site,
    }
    return render_template('critterring-widget.html', **context)






@app.route('/critterring.json')
def serve_critterring_json():
    # Path to your critterring.json file
    file_path = os.path.join('critterring.json')
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = file.read()  # Reading the content of the file
        
        return jsonify(data)  # Returns the data as JSON
    else:
        return jsonify({"error": "File not found"}), 404
'''
ALLOWED_FILES = [
    'critterring-style.css',
    'critterring-layout.css',
    'critterring-index.js',
    'critterring-variables.js',
    'critterring-widget.js'
]'''

@app.route('/<file_name>')
def serve_static_file(file_name):
    file_type = file_name.split(".")[-1]
    folder = os.path.join(STATIC_FOLDER, file_type)
    print(str(folder))
    return send_from_directory(folder, file_name)

@app.route('/images/<file_name>')
def serve_static_image(file_name):
    folder = os.path.join(STATIC_FOLDER, "images" )

    return send_from_directory(folder, file_name) or 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure all tables are created
    app.run(debug=True, port="1000")



@app.errorhandler(400)
def handle_bad_request(error):
    return "Bad Request (Possible CSRF Attack)", 400

