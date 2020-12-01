from flask import Flask
from flask_restful import Api, Resource, reqparse
import mariadb
import sys
import json, os
from bson import json_util, ObjectId

app = Flask(__name__)
api = Api(app)

try:
    conn = mariadb.connect(
        user="squad3",
        password="Broodjekoek!12",
        host="192.168.50.69",
        port=3307,
        database="kniptoptijd"

    )
except mariadb.Error as e:
    print(f"Error connecting to mariadb platform: {e}")
    sys.exit(1)  

else:
    print ("it works!")

cur = conn.cursor()