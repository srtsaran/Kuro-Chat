from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="static")  # Serve static files from 'static' folder
CORS(app)

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    payload = {
        "model": "meta-llama-3-8b-instruct",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7,
        "max_tokens": 200
    }

    response = requests.post(LM_STUDIO_URL, json=payload)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
