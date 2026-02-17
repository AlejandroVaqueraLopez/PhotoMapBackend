from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import json
import io
import base64
 
'''#def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = {}
        info = image._getexif()
    
        if not info:
             return {
                "hasExif": False,
                "metadata": None,
                "latitude": None,
                "longitude": None
            }
    
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
    
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data["GPSInfo"] = gps_data
            else:
                exif_data[decoded] = value

        lat, lon = get_coordinates(exif_data.get("GPSInfo"))

        return {
            "hasExif": True,
            "metadata": exif_data,
            "latitude": lat,
            "longitude": lon
        }
    
    except Exception as e:
        return {
            "error": str(e)
        }

''' 
def convert_to_degrees(value):
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except Exception:
        return None
 
def get_coordinates(gps_info):
    if not gps_info:
        return None, None
 
    try:
        lat = convert_to_degrees(gps_info.get("GPSLatitude"))
        if gps_info.get("GPSLatitudeRef") != "N":
            lat = -lat
 
        lon = convert_to_degrees(gps_info.get("GPSLongitude"))
        if gps_info.get("GPSLongitudeRef") != "E":
            lon = -lon
 
        return lat, lon
 
    except Exception:
        return None, None
 #en lugar de eso, recibir la imagen
 #lat, lng <-
 #almacenar todo dentro de funcion, recibe imagen y retorno json completo  y lo recibe para agregar foto
'''
def get_image(image_bytes):

    image = Image.open(io.BytesIO(image_bytes))
    exif = get_exif_data(image)
    
    if not exif:
        #print("Photo has not metadata EXIF")
        return {
            "hasExif": False,
            "latitude": None,
            "longitude": None
        }
    else:
        lat, lon = get_coordinates(exif.get("GPSInfo"))
    
        if lat is not None and lon is not None:
            #print("Latitude:", lat)
            #print("Longitude:", lon)
            #print(f"Google Maps: https://www.google.com/maps?q={lat},{lon}")
            #print(get_coordinates(exif.get("GPSInfo")))
            
            metadata_json = {
            "hasExif": True,
            "metadata": exif,
            "date": exif.get("DateTimeOriginal"),
            "latitude": lat,
            "longitude": lon
        }
        else:
            print("There is not GPS info...")

        return metadata_json bro i hate this fr'''

def make_json_serializable(data):
    if isinstance(data, dict):
        return {k: make_json_serializable(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [make_json_serializable(i) for i in data]
    elif isinstance(data, tuple):
        return tuple(make_json_serializable(i) for i in data)
    else:
        try:
            json.dumps(data)
            return data
        except TypeError:
            return str(data)


def get_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        exif_data = {}
        info = image._getexif()

        if not info:
            return {
                "hasExif": False,
                "metadata": None,
                "latitude": None,
                "longitude": None
            }

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)

            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data["GPSInfo"] = gps_data
            else:
                exif_data[decoded] = value

        lat, lon = get_coordinates(exif_data.get("GPSInfo"))

        return make_json_serializable({
            "hasExif": True,
            #"metadata": exif_data,
            "latitude": lat,
            "longitude": lon
        })


    except Exception as e:
        return {
            "error": str(e)
        }
