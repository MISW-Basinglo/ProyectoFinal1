from flask import Flask, redirect, url_for, session, request, jsonify
from oauthlib.oauth2 import WebApplicationClient
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de Google OAuth 2.0
CLIENT_ID = "TU_CLIENT_ID"
CLIENT_SECRET = "TU_CLIENT_SECRET"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Cliente de OAuth 2.0
client = WebApplicationClient(CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/")
def index():
    return "Bienvenido. <a href='/login'>Inicia sesión con Google</a>"

@app.route("/login")
def login():
    # Descubre los endpoints de Google para OAuth
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Redirige al usuario a Google para la autenticación
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Obtén el código de autorización que envía Google
    code = request.args.get("code")

    # Obtén los tokens de Google
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

    # Parseamos la respuesta de tokens
    client.parse_request_body_response(token_response.text)

    # Ahora obtén la información del usuario
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Verifica el correo del usuario
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        return jsonify({"email": users_email, "name": users_name})
    else:
        return "Error: El correo no está verificado por Google.", 400

if __name__ == "__main__":
    app.run(ssl_context="adhoc")  # SSL es requerido por Google para OAuth
