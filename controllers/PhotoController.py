from flask import Blueprint, request, jsonify, g
import json
import os
import hashlib
from models.Photo import Photo, RecordNotFoundException
from security.auth import generate_token, require_auth
from services.Metadata import get_image
from models.Location import Location
from dotenv import load_dotenv
load_dotenv()
from services.Geocoding import reverse_geocode

# Export to server
photo_bp = Blueprint('photo_bp', __name__)
 
# GET ALL (/photos)
@photo_bp.route("/photos", methods=["GET"])
@require_auth
def get_photos():
    try:
        return jsonify({
            "status": 0,
            "data": [json.loads(p.to_json()) for p in Photo.get_all()]
        })
    except Exception as e:
        return jsonify({
            "status": 1,
            'errorMessage' : str(e)
        })
  
#POST
@photo_bp.route("/photos", methods=["POST"])
@require_auth
def add():
    try:
        file = request.files.get("photo")
        user_id = request.user_id
        title = request.form.get("title")
        description = request.form.get("description")

        if not file:
            return jsonify({"status": 1, "errorMessage": "No file provided"})

        image_bytes = file.read()

        #generate hash
        file_hash = hashlib.sha256(image_bytes).hexdigest()

        #checking if exists before saving
        existing_photo = Photo.get_by_hash(file_hash)

        if existing_photo:
            return jsonify ({
                "status":1,
                "errorMessage": "This photo was already uploaded"
            })

        filename = f"{file_hash}.jpg"
        upload_path = os.path.join("uploads", filename)

        #save
        with open(upload_path, "wb") as f:
            f.write(image_bytes)

        #read metadata
        metadata = get_image(image_bytes)

        #latitude
        lat = metadata.get("latitude")
        #longitude
        lng = metadata.get("longitude")
        if lat is None or lng is None:
            return jsonify({"status": 1, "errorMessage": "Image has no GPS metadata"})
        
        #checking if a location with those coordinates already exists
        location = Location.get_by_coordinates(lat, lng)

        if not location:
            location = Location()
            geo_data = reverse_geocode(lat, lng)
            if geo_data and geo_data.get("formatted_address"):
                location.name = geo_data["formatted_address"]
                location.address = geo_data["formatted_address"]
            else:
                location.name = "Unknown location"
                location.address = ""
            location.lat = lat
            location.lng = lng
            location.status = 1
            location.add()

        #create photo
        p = Photo()
        p.userID = user_id
        p.title = title
        p.description = description
        p.imagePath = filename
        p.createdAt = None
        p.locationID = location.id
        p.fileHash = file_hash

        p.add()

        return jsonify({
            "status": 0,
            "message": "Photo uploaded successfully",
            "locationID": location.id
        })

    except Exception as e:
        return jsonify({
            "status": 1,
            "errorMessage": str(e)
        })

#GET /photo/id
@photo_bp.route('/photos/<int:photo_id>', methods=['GET'])
@require_auth
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

        p.title = data.get("title")
        p.description = data.get("description")

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
