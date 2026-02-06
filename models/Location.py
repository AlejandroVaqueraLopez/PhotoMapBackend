#import class
from .SQLServerConnection import SQLServerConnection
from .User import User
import json

# record not found exception
class RecordNotFoundException(Exception):
    pass

class Location:
    #attributes
    def __init__(self, *args):
        self._id = 0
        self._name = ""
        self._description = ""
        self._address = ""
        self._lat = 0.0
        self._lng = 0.0
        self._photo = ""
        self._userID = None #objeto de clase usuario
        self._status = 1

        #parameters = 9
        if len(args) == 9:
            self._id, self._name, self._description, self._address, self._lat, self._lng, self._photo, self._userID, self._status = args
        elif len(args) == 1:
            self.load_by_id(args[0])

    #properties
    @property
    def id(self): return self._id
    @id.setter
    def id(self, value): self._id = value

    @property
    def name(self): return self._name
    @name.setter
    def name(self, value): self._name = value

    @property
    def description(self): return self._description
    @description.setter
    def description(self, value): self._description = value

    @property
    def address(self): return self._address
    @address.setter
    def address(self, value): self._address = value

    @property
    def lat(self): return self._lat
    @lat.setter
    def lat(self, value): self._lat = value

    @property
    def lng(self): return self._lng
    @lng.setter
    def lng(self, value): self._lng = value

    @property
    def photo(self): return self._photo
    @photo.setter
    def photo(self, value): self._photo = value

    @property
    def userID(self): return self._userID
    @userID.setter
    def userID(self, value): self._userID = value

    @property
    def status(self): return self._status
    @status.setter
    def status(self, value): self._status = value

# load location by id
    def load_by_id(self, id):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "Select Id, Name, Description, Address, Lat, Lng, Photo, UserID, Status From Locations Where Id = ?",
                    (id)
                )
                row = cursor.fetchone()
                if row:
                    self._id, self._name, self._description, self._address, self._lat, self._lng, self._photo, user_id, self._status = row
                    self._userID = User(user_id)
                else:
                    raise RecordNotFoundException(f"Location with id {id} was not found.")
        except Exception as ex:
            raise ex

    #parse to json
    def to_json(self):
        return json.dumps(
            {
                "id": self._id,
                "name": self._name,
                "description": self._description,
                "address": self._address,
                "lat": float(self._lat) if self._lat is not None else None,
                "lng": float(self._lng) if self._lng is not None else None,
                "photo": self._photo,
                "status": self._status,
                "user": json.loads(self._userID.to_json()) if isinstance(self._userID, User) else self._userID
            }
        )

    #get all locations
    @staticmethod
    def get_all():
        list = []
        try:
            with SQLServerConnection.get_connection() as conn:

                cursor = conn.cursor()

                cursor.execute(
                    "Select Id, Name, Description, Address, Lat, Lng, Photo, UserID, Status From Locations Order By Name"
                )

                for row in cursor.fetchall():
                    location = Location(*row)
                    location._userID = User(location._userID)
                    list.append(location)

        except Exception as ex:
            print("Error fetching locations...", ex)

        return list

    def add(self):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                #self._userID = User()
                print(self._lat)
                cursor.execute(
                    "Insert Into Locations (Name, Description, Address, Lat, Lng, Photo, UserID, Status) Values (?, ?, ?, ?, ?, ?, ?, ?)",
                    (self._name, self._description, self._address, self._lat, self._lng, self._photo, self._userID, self._status)
                )
        except Exception as ex:
            raise ex

    #get locations by user
    @staticmethod
    def get_locations_by_user(user_id):
        list = []
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "Select Id, Name, Description, Address, Lat, Lng, Photo, UserID, Status "
                    "From Locations Where UserID = ? Order By Name",
                    (user_id)
                )

                for row in cursor.fetchall():
                    location = Location(*row)
                    location._userID = User(location._userID)
                    list.append(location)

        except Exception as ex:
            print("Error fetching locations by user...", ex)

        return list