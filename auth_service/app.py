from flask import Flask, jsonify, request
import time
import uuid

app = Flask(__name__)

users = [
    {"id": 1, "username": "user1", "password": "pass1"},
    {"id": 2, "username": "user2", "password": "pass2"}
]

tokens = {}
TOKEN_EXPIRATION_SECONDS = 600

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
    
    # Verificar si el usuario ya existe
    if any(user['username'] == data['username'] for user in users):
        return jsonify({'error': 'Username already exists'}), 409
    
    user_id = len(users) + 1
    new_user = {
        'id': user_id,
        'username': data['username'],
        'password': data['password']
    }
    
    users.append(new_user)
    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201

@app.route('/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = next((user for user in users if user['username'] == request.json['username']), None)
    if not user or user['password'] != request.json['password']:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Generar token único
    token = str(uuid.uuid4())
    expires = time.time() + TOKEN_EXPIRATION_SECONDS
    tokens[token] = {"user_id": user['id'], "username": user['username'], "expires": expires}
    
    return jsonify({
        "message": "Logged in successfully", 
        "token": token,
        "user_id": user['id'],
        "username": user['username']
    }), 200

@app.route('/validate_token', methods=['POST'])
def validate_token():
    data = request.json
    if not data or 'token' not in data:
        return jsonify({"error": "Token requerido"}), 400
    
    token = data.get("token")
    
    # Limpiar el Bearer si viene en el token
    if token.startswith('Bearer '):
        token = token[7:]
    
    if not token or token not in tokens:
        return jsonify({"error": "Token inválido"}), 403
    
    if time.time() > tokens[token]['expires']:
        del tokens[token]  # Limpiar token expirado
        return jsonify({"error": "Token expirado"}), 403
    
    return jsonify({
        "message": "Token válido",
        "user_id": tokens[token]['user_id'],
        "username": tokens[token]['username']
    }), 200

@app.route('/logout', methods=['POST'])
def logout():
    data = request.json
    if not data or 'token' not in data:
        return jsonify({"error": "Token requerido"}), 400
    
    token = data.get("token")
    if token.startswith('Bearer '):
        token = token[7:]
    
    if token in tokens:
        del tokens[token]
        return jsonify({"message": "Logged out successfully"}), 200
    else:
        return jsonify({"error": "Token no encontrado"}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "service": "auth_service",
        "status": "running",
        "active_tokens": len(tokens)
    }), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)