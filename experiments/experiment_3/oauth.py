from flask import Flask, redirect, session, request, jsonify
from oauthlib.oauth2 import WebApplicationClient
import requests
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
# Configura la URL de la base de datos, utilizando postgresql://
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5480/users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)

# Configuración de Google OAuth 2.0
CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Cliente de OAuth 2.0
client = WebApplicationClient(CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.before_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return "Bienvenido. <a href='/login'>Iniciar Sesión con Google</a>"

@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
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
        auth=(CLIENT_ID, CLIENT_SECRET),
    )

    client.parse_request_body_response(token_response.text)

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]

        # Almacena el usuario en la base de datos
        user = User.query.filter_by(email=users_email).first()
        if not user:
            user = User(email=users_email, name=users_name, role='user')
            db.session.add(user)
            db.session.commit()

        session['user_email'] = users_email
        return jsonify({"email": users_email, "name": users_name, "role": user.role})
    else:
        return "Error: El correo no está verificado por Google.", 400

def requires_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_email = session.get('user_email')
            user = User.query.filter_by(email=user_email).first()
            if user is None or user.role != role:
                return jsonify({"message": "Access denied"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/admin")
@requires_role('admin')
def admin_resource():
    return "This is the admin resource."

@app.route("/user")
@requires_role('user')
def user_resource():
    return "This is the user resource."

if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context="adhoc")
