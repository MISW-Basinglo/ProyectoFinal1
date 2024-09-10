from flask import Flask, jsonify
import time
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/process', methods=['POST'])
def process():
    time.sleep(1)
    return jsonify({"message": "Processed successfully"}), 200

@app.route('/crash', methods=['GET'])
def crash():
    time.sleep(1)
    os._exit(1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
