from flask import Flask,jsonify,session,request
from controllers.UserController import user_bp
from controllers.LocationController import location_bp
from controllers.PhotoController import photo_bp
from security.auth import require_auth, generate_token
from models.User import User
import os
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = "super_secret_key"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Crear carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

from flask_cors import CORS

app.register_blueprint(user_bp)
app.register_blueprint(location_bp)
app.register_blueprint(photo_bp)

@app.route('/')
def home():
    return {
        "status": "ok",
        "message": "Hello World"
    }

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
#CORS(app, supports_credentials=True, origins=['http://127.0.0.1:5555'])

@app.route("/dashboard")#to get the data from logsession
@require_auth
def dashboard():
    return jsonify({
        "status": 0,
        "message": f"Welcome user"
    })

'''
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:

        token = generate_token(user.id)

        response = jsonify({"message": "Login successful"})
        response.set_cookie(
            "auth_token",
            token,
            httponly=True,
            samesite="Lax"
        )

        return response, 200

    return jsonify({"error": "Invalid credentials"}), 401
'''

@app.route("/me")
@require_auth
def get_current_user():
    try:
        user = User.get_by_id(request.user_id)
        return jsonify({
            "id": user.id,
            "username": user.username,
            "name":user.name,
            "lastname":user.lastname,
            "email":user.email
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

'''@app.after_request
def add_Cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE"
    return response

'''

app.run(port=5555, debug=True)
