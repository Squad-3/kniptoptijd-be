from flask import Flask
from flask_mail import Mail, Message
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'squad3test@gmail.com'
app.config['MAIL_PASSWORD'] = 'Broodjekoek112'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/mail")
def get():
   return post()

def post():
   parser = reqparse.RequestParser()
   parser.add_argument("email")
   parser.add_argument("naam")
   args = parser.parse_args() 
   recipients = [args["email"]]
   klant = [args["naam"]]   
   msg = Message('Kappersafspraak', sender = 'squad3test@gmail.com', recipients = recipients)
   msg.body = """Beste klant u heeft dag een afspraak om tijd bij kapsalon. U gaat behandeling bij kapper. Met vriendelijke groet, kapsalon"""
   mail.send(msg)
   return recipients, klant, "E-mail is verzonden"


# @app.route("/mail")
# def send_email():
#     recipients = "email"
#     msg = Message('Hello', sender= 'squad3test@gmail.com', recipients=recipients)
#     msg.body = "Hello Flask message sent from Flask-Mail"
#     mail.send(msg)

if __name__ == '__main__':
   app.run(debug = True)