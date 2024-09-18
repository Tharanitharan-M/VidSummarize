from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
import os
from chatbot import TranscriptChatbot

# Allow OAuth over HTTP for development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Google OAuth2 credentials
GOOGLE_CLIENT_ID = "GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "GOOGLE_CLIENT_SECRET"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(GOOGLE_CLIENT_ID)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)  # Nullable for Google login

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.password is None:
            return render_template('login.html', login_error='Signin with Google')
        if user and check_password_hash(user.password, password):
            session['user'] = {'name': user.name, 'email': user.email}
            return redirect(url_for('dashboard'))

        else:
            return render_template('login.html', login_error='Invalid email or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('signup.html', signup_error='Passwords do not match')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', signup_error='Email already exists')

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session['user'] = {'name': name, 'email': email}
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/login/google')
def google_login():
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect( )

@app.route('/login/google/callback')
def google_callback():
    code = request.args.get("code")
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]

        user = User.query.filter_by(email=users_email).first()
        if not user:
            user = User(name=users_name, email=users_email)
            db.session.add(user)
            db.session.commit()

        session['user'] = {'name': users_name, 'email': users_email}
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', login_error='Google authentication failed')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/chat', methods=["POST"])
def chat():
    user_input = request.form.get("user_input")
    if not user_input:
        return jsonify({"error": "Empty input"}), 400
    
    return jsonify({"response": chatbot.start_chat(user_input)})


if __name__ == '__main__':
    chatbot = TranscriptChatbot()
    app.run(debug=True)