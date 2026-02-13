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
        self._imageData = ""
        self._contentType = ""
        self._createdAt = ""
        self._locationID = None #clase Location

        #parameters
        if len(args) == 7:
            self._id, self._userID, self._title, self._imageData, self._contentType, self._createdAt ,self._locationID = args
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
    def imageData(self): return self._imageData
    @imageData.setter
    def imageData(self,value): self._imageData = value

    @property
    def contentType(self): return self._contentType
    @contentType.setter
    def contentType(self,value): self._contentType = value

    @property
    def createdAt(self): return self._createdAt
    @createdAt.setter
    def createdAt(self, value): self._createdAt = value

    @property
    def locationID(self): return self._locationID
    @locationID.setter
    def locationID(self, value): self._locationID = value

    #load by id
    def load_by_id(self, photo_id):
        try:
            with SQLServerConnection.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT PhotoID, UserID, Title, ImageData, ContentType, CreatedAt, LocationID FROM Photos Where PhotoID = ?",
                        photo_id
                    )
                    row = cursor.fetchone()
                    if row :
                        self.id, self.userID, self.title, self.imageData, self.contentType, self.createdAt, self.locationID = row
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
                    "imageData":self._imageData,
                    "contentType": self._contentType,
                    "createdAt":self._createdAt,
                    "LocationID":self._locationID
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
                        "SELECT PhotoID, UserID, Title, ImageData, ContentType, CreatedAt, LocationID FROM Photos Order By Title"
                    )
                    for row in cursor.fetchall():
                        list.append(Photo(*row))

            except Exception as ex:
                print("Error fetching photos...", ex)
            return list
    
    #add (create) 
    #recibir como parametro la foto
    #almacenar json completo
    #recibir foto y guardarlo en imageData como json
    def add(self):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Photos (UserID, Title, ImageData, ContentType, CreatedAt,LocationID) Values (?, ?, ?, ?, ?,?)",
                   (self._userID, self._title, self._imageData, self._contentType, self._createdAt, self._locationID)
            )
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
                    SET UserID = ?, Title = ?, ImageData = ?, ContentType = ?, CreatedAt = ?, LocationID = ?
                    WHERE PhotoID = ?""",
                    (self._userID, self._title, self._imageData,
                    self._contentType, self._createdAt,
                    self._locationID, self._id)
                )
        except Exception as ex:
            raise ex
