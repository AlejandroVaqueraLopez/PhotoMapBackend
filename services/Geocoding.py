import requests
import os

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def reverse_geocode(lat, lng):
    if not lat or not lng:
        return None

    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "latlng": f"{lat},{lng}",
            "key": GOOGLE_MAPS_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "OK":
            print("Google error:", data)
            return None

        result = data["results"][0]

        return {
            "formatted_address": result.get("formatted_address")
        }

    except Exception as e:
        print("Reverse geocode exception:", e)
        return None
