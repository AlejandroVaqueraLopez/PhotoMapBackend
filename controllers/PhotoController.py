from flask import Blueprint, request, jsonify
import json
import uuid
import os
from models.Photo import Photo, RecordNotFoundException
from services.Metadata import get_image
from models.Location import Location


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
            'errorMessage' : str(e)
        })
  
#POST
@photo_bp.route("/photos", methods=["POST"])
def add():
    try:
        file = request.files.get("photo")
        user_id = request.form.get("userID")
        title = request.form.get("title")
        description = request.form.get("description")

        if not file:
            return jsonify({"status": 1, "errorMessage": "No file provided"})

        #generate unique name
        filename = f"{uuid.uuid4()}.jpg"
        upload_path = os.path.join("uploads", filename)
        #save
        file.save(upload_path)
        #read metadata
        image_bytes = open(upload_path, "rb").read()
        metadata = get_image(image_bytes)

        #latitude
        lat = metadata.get("latitude")
        #longitude
        lng = metadata.get("longitude")
        if lat is None or lng is None:
            return jsonify({"status": 1, "errorMessage": "Image has no GPS metadata"})
        
        #checking if a location with those coordinates already exists
        location = Location.get_by_coordinates(lat, lng)

        #if does not exist
        if not location:
            #new location
            location = Location()
            location.name = "Auto-generated location"
            #location.description = "Created from EXIF metadata" removed description
            location.address = ""
            location.lat = lat
            location.lng = lng
            location.photo = filename
            location.userID = user_id
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
        p.description = data.get("description")
        p.imagePath = data.get("imagePath")
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

''' OG
Para hacer POST a una foto, en postman se usa asi:
{
    "userID": 1,
    "title": "Test Photo",
    "imageData": "", <--AQUI PONER BASE64
    "contentType": "image/jpeg",
    "createdAt": "2026-02-14",
    "locationID": 1
}
'''

''' con foto

'''