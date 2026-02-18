from .SQLServerConnection import SQLServerConnection
import bcrypt
import json
from .User import User
from .Location import Location

from .SQLServerConnection import SQLServerConnection
#record not found exception
class RecordNotFoundException(Exception):
    pass

class Photo:
    def __init__(self, *args):
        self._id = 0
        self._userID = None #objeto de clase usuario
        self._title = ""
        self._description = ""
        self._imagePath = ""
        self._createdAt = ""
        self._locationID = None #clase Location
        self._fileHash = ""


        #parameters
        if len(args) ==8:
            self._id, self._userID, self._title, self._description, self._imagePath, self._createdAt ,self._locationID , self._fileHash= args
        elif len(args) == 1:
            self.load_by_id(args[0])

    #properties
    @property
    def id(self): return self._id
    @id.setter
    def id(self, value): self._id = value

    @property
    def userID(self): return self._userID
    @userID.setter
    def userID(self, value): self._userID = value

    @property
    def title(self): return self._title
    @title.setter
    def title(self, value): self._title = value

    @property
    def description(self): return self._description
    @description.setter
    def description(self, value): self._description = value

    @property
    def imagePath(self): return self._imagePath

    @imagePath.setter
    def imagePath(self, value): self._imagePath = value

    @property
    def createdAt(self): return self._createdAt
    @createdAt.setter
    def createdAt(self, value): self._createdAt = value

    @property
    def locationID(self): return self._locationID
    @locationID.setter
    def locationID(self, value): self._locationID = value

    @property
    def fileHash(self): return self._fileHash

    @fileHash.setter
    def fileHash(self, value): self._fileHash = value

    #load by id
    def load_by_id(self, photo_id):
        try:
            with SQLServerConnection.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT PhotoID, UserID, Title, Description, ImagePath, CreatedAt, LocationID , FileHash FROM Photos Where PhotoID = ?",
                        (photo_id,)
                    )
                    row = cursor.fetchone()
                    if row :
                        self.id, self.userID, self.title, self._description, self._imagePath, self.createdAt, self.locationID, self._fileHash = row
                    else:
                        raise RecordNotFoundException(f"Photo with id {photo_id} was not found.")  

        except Exception as e:
                raise e

    #to json
    def to_json(self):
            return json.dumps(
                {
                    "id":self._id,
                    "userID":self._userID,
                    "title": self._title,
                    "description":self._description,
                    "imagePath": self._imagePath,
                    "createdAt": self._createdAt.isoformat() if self._createdAt else None,
                    "LocationID":self._locationID,
                    "fileHash" : self._fileHash
                }
            )

    #get all (read)
    @staticmethod
    def get_all():

            list = []
            try:
                with SQLServerConnection.get_connection() as conn:
                    cursor = conn.cursor()

                    cursor.execute(
                        "SELECT PhotoID, UserID, Title, Description, ImagePath, CreatedAt, LocationID, FileHash FROM Photos ORDER BY Title"
                    )
                    for row in cursor.fetchall():
                        list.append(Photo(*row))

            except Exception as ex:
                print("Error fetching photos...", ex)
            return list
    
    #add (create) 
    #recibir como parametro la foto
    def add(self):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Photos (UserID, Title, Description, ImagePath, LocationID, FileHash) Values (?, ?, ?, ?, ?, ?)",
                   (self._userID, self._title, self._description ,self._imagePath, self._locationID, self._fileHash)
            )
            conn.commit()
        except Exception as ex:
            raise ex
        
    #delete
    def delete(self):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM Photos WHERE PhotoID = ?",
                    self._id
                )
        except Exception as ex:
            raise ex

   #modify
    def update(self):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                     """UPDATE Photos
                        SET Title = ?, Description = ?
                        WHERE PhotoID = ?""",
                    (self._title, self._description, self._id)
                )
        except Exception as ex:
            raise ex

    @staticmethod
    def get_by_hash(file_hash):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT TOP 1 PhotoID FROM Photos WHERE FileHash = ?",
                    (file_hash,)
                )
                return cursor.fetchone()
        except Exception as e:
            raise e

 #get by location
    @staticmethod
    def get_by_location(self, location_id):
        try:
            with SQLServerConnection.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT PhotoID, UserID, Title, Description, ImagePath, CreatedAt, LocationID , FileHash FROM Photos Where LocationID = ?",
                        (location_id,)
                    )
                    row = cursor.fetchone()
                    if row :
                        self.id, self.userID, self.title, self._description, self._imagePath, self.createdAt, self.locationID, self._fileHash = row
                    else:
                        raise RecordNotFoundException(f"Photo with location id {location_id} was not found.")  

        except Exception as e:
                raise e