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

@app.route('/afspraak', methods=['POST'])
def get_afspraak():
    return post_afspraak(cur)

def post_afspraak(cur):
    parser = reqparse.RequestParser()
    parser.add_argument("kapsalonid")
    parser.add_argument("behandelingid")
    args = parser.parse_args()
    cur.execute("""SELECT DISTINCT b.behandelingID, b.naam, b.prijs, k.kapperID, k.voornaam, k.werkdagen
                FROM KappersBehandelingen kb 
                JOIN Behandelingen b
                ON kb.behandelingID = b.behandelingID
                JOIN Kappers k
                ON kb.kapperID = k.kapperID
                WHERE kb.KapsalonID=?
                """, 
                (args['kapsalonid'],args['behandelingid'],))
    behandelingcollectie = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify(behandelingcollectie)
#if __name__ == '__main__':
app.run()
     