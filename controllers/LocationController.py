from flask import Blueprint, request, jsonify
import json
from models.Location import Location, RecordNotFoundException
from models.Photo import Photo
from security.auth import generate_token, require_auth
 
# Export to server
location_bp = Blueprint('location_bp', __name__)
 
# GET ALL (/locations)
@location_bp.route("/locations", methods=["GET"])
@require_auth
def get_locations():
    try:
        return jsonify({
            "status": 0,
            "data": [json.loads(t.to_json()) for t in Location.get_all()]
        })
    except Exception as e:
        return jsonify({
            "status": 1,
            'errorMessage' : str(e)
        })

# POST
@location_bp.route("/locations", methods=["POST"])
@require_auth
def add():
    try:
        data = request.get_json()

        # user object
        l = Location()

        l.name = data.get("name")
        l.address = data.get("address")
        l.lat = data.get("lat")
        l.lng = data.get("lng")
        l.status = data.get("status", 1)

        # send data
        l.add()

        return jsonify({
            "status": 0,
            "message": "Location added successfully"
        })

    except Exception as e:
        return jsonify({
            "status": 1,
            "errorMessage": str(e)
        })
    
# GET /location/id
@location_bp.route('/locations/<int:location_id>', methods=['GET'])
@require_auth
def get_location_by_id(location_id):
    try:
        t = Location(location_id)
        return jsonify({
            'status' : 0,
            'data': json.loads(t.to_json())
        })
    except Exception as e:
        return jsonify({
            'status':1,
            'errorMessage' : str(e)
        })

#get photos from location ID
@location_bp.route('/locations/<int:location_id>/photos', methods=['GET'])
def get_photos_by_location(location_id):
    try:
        photos = Photo.get_by_location(location_id)

        return jsonify({
            "status": 0,
            "data": [json.loads(p.to_json()) for p in photos]
        })

    except Exception as e:
        return jsonify({
            "status": 1,
            "errorMessage": str(e)
        })
