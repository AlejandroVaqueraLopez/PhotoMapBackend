from flask import Blueprint, request, jsonify
import json
from models.Photo import Photo, RecordNotFoundException

# Export to server
photo_bp = Blueprint('photo_bp', __name__)
 
# GET ALL (/photos)
@photo_bp.route("/photos", methods=["GET"])
def get_photos():
    try:
        return jsonify({
            "status": 0,
            "data": [json.loads(p.to_json()) for p in Photo.get_all()]
        })
    except Exception as e:
        return jsonify({
            "status": 1,
            'errorMessage' :(e)
        })

#POST
@photo_bp.route("/photos", methods=["POST"])
def add():
    try:
        data = request.get_json()

        # user object
        p = Photo()

        p.userID = data.get("userID")
        p.title = data.get("title")
        p.imageData = data.get("imageData")
        p.contentType = data.get("contentType")
        p.createdAt = data.get("createdAt")
        p.locationID = data.get("locationID")

        # send data
        p.add()

        return jsonify({
            "status": 0,
            "message": "Location added successfully"
        })

    except Exception as e:
        return jsonify({
            "status": 1,
            "errorMessage": str(e)
        })

#GET /photo/id
@photo_bp.route('/photos/<int:photo_id>', methods=['GET'])
def get_photo_by_id(photo_id):
    try:
        t = Photo(photo_id)
        return jsonify({
            'status' : 0,
            'data': json.loads(t.to_json())
        })
    except Exception as e:
        return jsonify({
            'status':1,
            'errorMessage' : str(e)
        })
    
#delete photo
@photo_bp.route('/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    try:
        p = Photo(photo_id)
        p.delete()

        return jsonify({
            "status": 0,
            "message": "Photo deleted successfully"
        })

    except Exception as e:
        return jsonify({
            "status": 1,
            "errorMessage": str(e)
        })


#modify photo
@photo_bp.route('/photos/<int:photo_id>', methods=['PUT'])
def update_photo(photo_id):
    try:
        data = request.get_json()

        p = Photo(photo_id)

        p.userID = data.get("userID")
        p.title = data.get("title")
        p.imageData = data.get("imageData")
        p.contentType = data.get("contentType")
        p.createdAt = data.get("createdAt")
        p.locationID = data.get("locationID")

        p.update()

        return jsonify({
            "status": 0,
            "message": "Photo updated successfully"
        })

    except Exception as e:
        return jsonify({
            "status": 1,
            "errorMessage": str(e)
        })
