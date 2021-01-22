from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import mariadb
import sys
import json
from flask_mail import Mail, Message
from settings import db_password, db_user, db_host
from bson import json_util, ObjectId
from mail import post_mail

app = Flask(__name__)
api = Api(app)
mail= Mail(app)
mail.init_app(app) 

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
    return jsonify(behandelingcollectie), 

@app.route('/afspraak', methods=['POST'])
def post_afspraak():
    parser = reqparse.RequestParser()
    parser.add_argument("kapsalonid")
    parser.add_argument("kapperid")
    parser.add_argument("behandelingid")
    parser.add_argument("dag")
    parser.add_argument("tijd")
    parser.add_argument("klant")
    parser.add_argument("klantemail")
    parser.add_argument("klanttelefoon")
    args = parser.parse_args()
    cur.execute("""INSERT INTO Afspraken (kapsalon, kapper, behandeling, dag, tijd, klant, klantemail, klanttelefoon)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, 
                (args['kapsalonid'],args['kapperid'],args['behandelingid'],args['dag'],args['tijd'],args['klant'],args['klantemail'],args['klanttelefoon']))
    post_mail()
    conn.commit()
    return "Afspraak aangemaakt"
 
@app.route('/afspraakvewijderen', methods=['DELETE'])
def delete_afspraakvewijderen():
    parser = reqparse.RequestParser()
    parser.add_argument("afspraakid")
    args = parser.parse_args()
    cur.execute("""DELETE FROM Afspraken
                WHERE afspraakID = ?
                """, 
                (args['afspraakid'],))
    conn.commit()
    return "Afspraak verwijderd"
#if __name__ == '__main__':
app.run()
     