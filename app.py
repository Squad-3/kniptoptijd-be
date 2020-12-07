from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import mariadb
import sys
import json
from settings import db_password, db_user, db_host
from bson import json_util, ObjectId

app = Flask(__name__)
api = Api(app) 

conn = mariadb.connect(
    user=db_user,
    password=db_password,
    host=db_host,
    port=3307,
    database="kniptoptijd")
cur = conn.cursor()

@app.route('/')
def get():
    cur.execute('''select * from Kappers''')
    r = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'kapperscollectie' : r})

#if __name__ == '__main__':
app.run()
     