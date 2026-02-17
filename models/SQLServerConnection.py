import os
import pyodbc
from dotenv import load_dotenv

#read env data
load_dotenv()

class SQLServerConnection:
    @staticmethod
    def get_connection():
        #read environment variables
        server = os.getenv("SQL_SERVER")
        database = os.getenv("SQL_DATABASE")
        username = os.getenv("SQL_USER")
        password = os.getenv("SQL_PASSWORD")

        #check parameters
        if not server:
            print("No server provided")
        if not database:
            print("No database provided")
        if not username:
            print("No user provided")
        if not password:
            print("No password provided")
        #connection string
        connectionString = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            #"TrusterServerCertificate=yes;"
        )

        #connection
        try:
            connection = pyodbc.connect(connectionString)
            #set utf-8 enconding/decoding
            connection.setencoding(encoding="utf-8")
            connection.setdecoding(pyodbc.SQL_CHAR, encoding="utf-8")
            connection.setdecoding(pyodbc.SQL_WCHAR, encoding="utf-8")
        except Exception as ex:
            print(str(ex))
            return None
        #return
        return connection



        '''

       connectionString = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-SAGTNI8\\SQLEXPRESS;"
            "DATABASE=master;"
            "UID=sa;"
            "PWD=Mango2003A;"
        )


        try:
            conn = pyodbc.connect(connectionString, timeout=5)
            print("Conectado a master como sa")
            conn.close()
        except Exception as e:
            print("Error:eeeeeeeeeee", e)

        '''

