from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_SERVICE_URL = "http://auth_service:5001"  # URL del microservicio de autenticación

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    # Llamada al servicio de autenticación
    response = requests.post(f"{AUTH_SERVICE_URL}/login", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/resource', methods=['GET'])
def access_resource():
    token = request.headers.get('Authorization')
    response = requests.get(f"{AUTH_SERVICE_URL}/authorize", headers={'Authorization': token})
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
