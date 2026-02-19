from flask import Blueprint, request, jsonify, make_response
import json
from models.User import User, RecordNotFoundException
from security.auth import generate_token, require_auth

# Export to server
user_bp = Blueprint('user_bp', __name__)

# GET ALL (/Users)
@user_bp.route("/users", methods=["GET"])
@require_auth #we are calling our own function
def get_users():
    try:
        return jsonify({
            "status": 0,
            "data": [json.loads(u.to_json()) for u in User.get_all()]
        })
    except Exception as e:
        return jsonify({
            "status": 1,
            'errorMessage': str(e)
        })


# GET /users/id
@user_bp.route('/users/<int:user_id>', methods=['GET'])
@require_auth
def get_user_by_id(user_id):
    try:
        u = User(user_id)
        return jsonify({
            'status': 0,
            'data': json.loads(u.to_json())
        })
    except Exception as e:
        return jsonify({
            'status': 1,
            'errorMessage': str(e)
        })

# add new user POST
@user_bp.route("/users", methods=["POST"])
@require_auth
def add():
    try:
        data = request.get_json()

        # user object
        u = User()

        u.name = data.get("name")
        u.lastname = data.get("lastname")
        u.email = data.get("email")
        u.username = data.get("username")
        u.password = data.get("password")
        u.status = data.get("status", 1)

        # send data
        u.add()

        return jsonify({
            "status": 0,
            "message": "User added successfully"
        })

    except Exception as e:
        return jsonify({
            "status": 1,
            "errorMessage": str(e)
        })

#log in
@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data or "username" not in data or "password" not in data:
            return jsonify({
                'status' : 1,
                'errorMessage' : "username and password are required"
            }), 400

        u = User.get_by_username(data["username"])
        if not u or not u.check_password(data["password"]):
            return jsonify({
                'status' : 1,
                'errorMessage': 'Invalid credentials'
            }), 401

        token = generate_token(u.id)

        response = make_response(jsonify({
            'status': 0,
            'user': json.loads(u.to_json())
        }))

        response.set_cookie(
            "auth_token",
            token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age= 60 * 60 * 10
        )
        return response
    except Exception as ex:
        return jsonify({
            'status': 2,
            "errorMessage": str(ex)
        }), 400

#log out
@user_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({
        'status': 0,
        'message': 'logged out'
    })
    response.delete_cookie("auth_token")
    return response


#delete (change status to 0)
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@require_auth
def delete_user(user_id):
    try:
        u = User(user_id)
        u.delete()  # soft delete

        return jsonify({
            "status": 0,
            "message": "User deleted successfully"
        })
    except Exception as e:
        return jsonify({
            "status": 1,
            "errorMessage": str(e)
        })

#update
@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@require_auth
def update_user(user_id):
    try:
        data = request.get_json()

        u = User(user_id)

        u.name = data.get("name", u.name)
        u.lastname = data.get("lastname", u.lastname)
        u.email = data.get("email", u.email)
        u.username = data.get("username", u.username)

        if "password" in data and data["password"]:
            u.password = data["password"]

        u.status = data.get("status", u.status)

        u.update()

        return jsonify({
            "status": 0,
            "message": "User updated successfully"
        })

    except Exception as e:
        return jsonify({
            "status": 1,
            "errorMessage": str(e)
        })
