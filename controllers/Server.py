from flask import Flask
from controllers.UserController import user_bp
from controllers.TaskController import task_bp

app = Flask(__name__)

# Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)


# Root (localhost:5002)
@app.route("/")
def home():
    return {
        "status": 0,
        "message": "Server is now up and running..."
    }


# CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='127.0.0.1', port=5002, debug=True)
    # app.run(port=5001, debug=True)
