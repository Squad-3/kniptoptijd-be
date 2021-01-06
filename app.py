from flask import Flask, jsonify, request
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

@app.route('/locatie', methods=['POST'])
def get_locatie():
    return post_locatie(cur)

def post_locatie(cur):
    parser = reqparse.RequestParser()
    parser.add_argument("locatie")
    args = parser.parse_args()
    #cur.execute("select * from Kappers where stad=? OR straatnaam=?", ('%' + args['locatie'] + '%','%' + args['locatie'] + '%'))
    cur.execute("select * from Kapsalons where ? IN (stad,straatnaam)", (args['locatie'],))
    kapperscollectie = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify(kapperscollectie)


@app.route('/behandeling', methods=['POST'])
def get_behandeling():
    return post_behandeling(cur)

def post_behandeling(cur):
    parser = reqparse.RequestParser()
    parser.add_argument("idkapsalon")
    args = parser.parse_args()
    #cur.execute("select * from Behandelingen where kapsalonID=?", (args['idkapsalon'],))
    cur.execute("""SELECT DISTINCT B.behandelingID, B.naam, B.prijs, B.tijd 
                FROM Behandelingen B INNER JOIN KappersBehandelingen K 
                ON B.behandelingID = K.behandelingID WHERE K.kapsalonID=?""", 
                (args['idkapsalon'],))
    behandelingcollectie = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify(behandelingcollectie)

@app.route('/kapper', methods=['POST'])
def get_kappers():
    return post_kappers(cur)

def post_kappers(cur):
    parser = reqparse.RequestParser()
    parser.add_argument("idkapsalon")
    parser.add_argument("idbehandeling")
    args = parser.parse_args()
    #cur.execute("select * from Kappers where kapsalonID=?", (args['idkapsalon'],))
    #cur.execute("select KA.kapperID, KA.kapsalonID, KA.behandelingID, KA.voornaam, KA.werkdagen from Kappers KA INNER JOIN Kapsalons K ON KA.kapsalonID = K.kapsalonID INNER JOIN Behandelingen B ON KA.behandelingID = B.behandelingID where K.kapsalonID=? ORDER BY kapperID", (args['idkapsalon'],))
    cur.execute("""SELECT DISTINCT KA.kapperID, KA.voornaam, KA.werkdagen
                FROM Kappers KA INNER JOIN KappersBehandelingen K
                ON KA.kapperID = K.kapperID
                INNER JOIN KappersKapsalons KS
                ON KA.kapperID = KS.kapperID 
                WHERE KS.kapsalonID=? AND K.behandelingID=?""", 
                (args['idkapsalon'], args['idbehandeling'],))
    behandelingcollectie = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify(behandelingcollectie)    
#if __name__ == '__main__':
app.run()
     