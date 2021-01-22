from flask import Flask, request
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

def post_mail():
   recipients = request.args.get('klantemail')
   dag = request.args.get('dag')
   tijd = request.args.get('tijd')
   kapsalon = request.args.get('kapsalonid')
   behandeling = request.args.get('behandelingid')
   kapper = request.args.get('kapperid')
   msg = Message('Kappersafspraak', sender = 'squad3test@gmail.com', recipients = [recipients])
   msg.body = 'Beste klant u heeft '+dag+' een afspraak om '+tijd+' bij '+kapsalon+'. U gaat '+behandeling+' bij '+kapper+'. Met vriendelijke groet, '+kapsalon+''
   mail.send(msg)
   return "sent"

if __name__ == '__main__':
   app.run(debug = True)


# @app.route("/mail")
# def send_email():
#     recipients = "email"
#     msg = Message('Hello', sender= 'squad3test@gmail.com', recipients=recipients)
#     msg.body = "Hello Flask message sent from Flask-Mail"
#     mail.send(msg)