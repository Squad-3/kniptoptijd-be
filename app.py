from flask import Flask
from flask_restful import Api, Resource, reqparse
import mariadb
import sys
import json, os
from bson import json_util, ObjectId

app = Flask(__name__)
api = Api(app)

conn = mariadb.connect(
    user="squad3",
    password="Broodjekoek!12",
    host="83.85.148.135",
    port=3307,
    database="kniptoptijd")
cur = conn.cursor()