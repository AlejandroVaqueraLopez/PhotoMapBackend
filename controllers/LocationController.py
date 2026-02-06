from flask import Blueprint, request, jsonify
import json
from models.Location import Location, RecordNotFoundException
 
# Export to server
location_bp = Blueprint('location_bp', __name__)
 
# GET ALL (/locations)
@location_bp.route("/locations", methods=["GET"])
def get_locations():
    try:
        return jsonify({
            "status": 0,
            "data": [json.loads(t.to_json()) for t in Location.get_all()]
        })
    except Exception as e:
        return jsonify({
            "status": 1,
            'errorMessage' :(e)
        })

# POST
@location_bp.route("/locations", methods=["POST"])
def add():
    try:
        data = request.get_json()

        # user object
        l = Location()

        l.name = data.get("name")
        l.description = data.get("description")
        l.address = data.get("address")
        l.lat = data.get("lat")
        l.lng = data.get("lng")
        l.photo = data.get("photo")
        l.userID = data.get("userID")
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
    
#POST
'''post will go here :3'''