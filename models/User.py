#import sql server connection class
import bcrypt
import json

from .SQLServerConnection import SQLServerConnection

#record not found exception
class RecordNotFoundException(Exception):
    pass

class User:
    def __init__(self, *args):
        self._id=0
        self._name=""
        self._lastname=""
        self._dateOfBirth=""
        self._username=""
        self._password=""
        self._phone=""
        self._status=1

        #constructors
        if(len(args) == 1):
            self.load_by_id(args[0])
        elif len(args) == 8:
            self._id, self._name, self._lastname, self._dateOfBirth, self._username, self._password, self._phone, self._status = args

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self,value):
        self._id = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name = value

    @property
    def lastname(self):
        return self._lastname
    @lastname.setter
    def lastname(self,value):
        self._lastname = value

    @property
    def dateOfBirth(self):
        return self._dateOfBirth
    @dateOfBirth.setter
    def dateOfBirth(self,value):
        self._dateOfBirth = value

    @property
    def username(self):
        return self._username
    @username.setter
    def username(self,value):
        self._username = value

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,value):
        if value:
            hashed = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
            self._password = hashed.decode('utf-8')

    @property
    def phone(self):
        return self._phone
    @phone.setter
    def phone(self,value):
        self._phone= value

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self,value):
        self._status = value

    def load_by_id(self,user_id):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "Select Id, Name, Lastname, DateOfBirth, Username, Password, Phone, Status From Users Where Id = ?",
                    user_id
                )
                row = cursor.fetchone()
                if row:
                    self._id, self._name, self._lastname, self._dateOfBirth, self._username, self._password, self._phone, self._status = row
                else:
                    raise RecordNotFoundException(f"User with id {user_id} was not found.")

        except Exception as e:
            raise e

    def to_json(self):
        return json.dumps(
            {
                "id":self._id,
                "name":self._name,
                "lastname":self._lastname,
                "dateOfBirth": self._dateOfBirth.isoformat() if self._dateOfBirth else None,
                "username":self._username,
                "phone":self._phone,
                "status":self._status
            }
        )

#GET ALL

    @staticmethod
    def get_all():
        list = []
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    "Select Id, Name, Lastname, DateOfBirth, Username, Password, Phone, Status From Users Order By Name,Lastname"
                )
                for row in cursor.fetchall():
                    list.append(User(*row))

        except Exception as ex:
            print("Error fetching users...", ex)
        return list

    def add(self):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "Insert Into Users (Name, Lastname, DateOfBirth, Username, Password, Phone, Status) Values (?, ?, ?, ?, ?, ?, ?)",
                    (self._name, self._lastname, self._dateOfBirth, self._username, self._password, self._phone, self._status)
                )
        except Exception as ex:
            raise ex

    #Login
    def get_by_username(username):
        try:
            with SQLServerConnection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "Select Id, Name, Lastname, DateOfBirth, Username, Password, Phone, Status From Users Where Username = ?",
                    (username)
                )
                row = cursor.fetchone()
                if row :
                    return User(*row)
        except Exception as e:
            pass
        return None

    #check password
    def check_password(self, plain_password):
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            self._password.encode("utf-8")
        )
