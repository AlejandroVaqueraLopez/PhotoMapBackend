from flask import Flask
from controllers.UserController import user_bp
from controllers.LocationController import location_bp
app = Flask(__name__)
from flask_cors import CORS

app.register_blueprint(user_bp)
app.register_blueprint(location_bp)
@app.route('/')
def home():
    return {
        "status": "ok",
        "message": "Hello World"
    }

CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
CORS(app, supports_credentials=True, origins=['http://127.0.0.1:5500'])

'''
@app.after_request
def add_Cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE"
    return response
    '''

app.run(host='localhost', port=5000, debug=True)
