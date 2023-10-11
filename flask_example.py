from flask import Flask, request, jsonify
import json
import os
import requests

app = Flask(__name__)

# Directory where files will be stored
STORE_DIR = "store"

# Ensure the storage directory exists
if not os.path.exists(STORE_DIR):
    os.mkdir(STORE_DIR)

# Bitbucket API Base URL
BITBUCKET_API_BASE_URL = "https://api.bitbucket.org/2.0"

@app.route('/api/v1/app/<app_code>/meta/', methods=['GET', 'POST'])
def handle_meta(app_code):
    file_path = os.path.join(STORE_DIR, f'{app_code}_meta.txt')
    
    if request.method == 'POST':
        meta_data = request.json
        with open(file_path, 'w') as f:
            json.dump(meta_data, f, indent=4)
        return jsonify({"message": "Data stored successfully"}), 200
    
    elif request.method == 'GET':
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                meta_data = json.load(f)
            return jsonify(meta_data), 200
        else:
            return jsonify({"message": "File not found"}), 404

@app.route('/api/v1/token/verify/', methods=['POST'])
def verify_token():
    # Assuming the Bitbucket API token is sent in the request's "Authorization" header as a bearer token
    bitbucket_token = request.headers.get("Authorization").replace("Bearer ", "")
    
    # Verify the Bitbucket API token by making an API request
    headers = {"Authorization": f"Bearer {bitbucket_token}"}
    response = requests.get(f"{BITBUCKET_API_BASE_URL}/user", headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        username = user_data.get("username")
        return jsonify({"verified": True, "username": username}), 200
    else:
        return jsonify({"verified": False, "error": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(debug=True)
