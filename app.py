from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import mariadb
import sys
import json
from settings import db_password, db_user, db_host


app = Flask(__name__)
api = Api(app) 

conn = mariadb.connect(
    user='squad3',
    password='Broodjekoek!12',
    host= '83.85.148.135',
    port=3307,
    database="kniptoptijd")
cur = conn.cursor()

t=('Utrecht',)

@app.route('/')
def get():
    cur.execute('''select * from Kappers where stad=?''', t)
    r = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'kapperscollectie' : r})

#if __name__ == '__main__':
app.run()
     