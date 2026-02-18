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
        self._address = ""
        self._lat = 0.0
        self._lng = 0.0
        self._status = 1

        #parameters = 6
        if len(args) == 6:
            self._id, self._name, self._address, self._lat, self._lng, self._status = args
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
    def status(self): return self._status
    @status.setter
    def status(self, value): self._status = value

# load location by id
    def load_by_id(self, id):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "Select LocationID, Name, Address, Lat, Lng, Status From Locations Where LocationID = ?",
                    (id)
                )
                row = cursor.fetchone()
                if row:
                    self._id, self._name, self._address, self._lat, self._lng, self._status = row
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
                "address": self._address,
                "lat": float(self._lat) if self._lat is not None else None,
                "lng": float(self._lng) if self._lng is not None else None,
                "status": self._status,
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
                    "Select LocationID, Name, Address, Lat, Lng, Status From Locations Order By Name"
                )

                for row in cursor.fetchall():
                    location = Location(*row)
                    list.append(location)

        except Exception as ex:
            print("Error fetching locations...", ex)

        return list

    #ADD locations
    def add(self):
        
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                #self._userID = User()
                #print(self._lat)
                cursor.execute(
                    "Insert Into Locations (Name, Address, Lat, Lng, Status) OUTPUT INSERTED.LocationID Values ( ?, ?, ?, ?,? )",
                    (self._name, self._address, self._lat, self._lng, self._status)
                )
                row = cursor.fetchone()
                self._id = row[0]

                conn.commit()

        except Exception as ex:
            raise ex

    '''
    #get locations by user
    @staticmethod
    def get_locations_by_user(user_id):
        list = []
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "Select Id, Name, Address, Lat, Lng, Status "
                    "From Locations Where UserID = ? Order By Name",
                    (user_id)
                )

                for row in cursor.fetchall():
                    location = Location(*row)
                    list.append(location)

        except Exception as ex:
            print("Error fetching locations by user...", ex)

        return list'''
    
    #search location based on lat and lng
    @staticmethod
    def get_by_coordinates(lat, lng):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT LocationID, Name, Address, Lat, Lng, Status "
                    "FROM Locations WHERE Lat = ? AND Lng = ?",
                    (lat, lng)
                )
                row = cursor.fetchone()
                if row:
                    return Location(*row)
                return None
        except Exception as e:
            raise e
