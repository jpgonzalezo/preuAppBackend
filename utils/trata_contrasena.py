import random
import string
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'soporte2030usach@gmail.com'
app.config['MAIL_PASSWORD'] = 'soporte.usach2030'
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)


def send_message(codigo, email):
    msg = Message('Hello from the other side!', sender = 'soporte2030usach@gmail.com', recipients = ['luis.migryk@usach.cl',email])
    msg.body = "Hey Cristian, tu codigo de recuperacion es:" + codigo
    mail.send(msg)
    return "Message sent!"


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))
    # print random string
    return(result_str)


def created_random_pass_by_profile(user_mail, admin, alumno, apoderado, profesor):
    provisional_pass = get_random_string(8)
    count_profile = 0
    if (admin != None):
        print("paso admin")
        count_profile += 1
        admin.create_provisional_pass(user_mail, provisional_pass)
    if (alumno != None):
        print("paso alumno")
        count_profile += 1
        alumno.create_provisional_pass(user_mail,provisional_pass)
    if (apoderado != None):
        print("paso apoderado")
        count_profile += 1
        apoderado.create_provisional_pass(user_mail,provisional_pass)
    if (profesor != None):
        print("paso profe")
        count_profile += 1
        profesor.create_provisional_pass(user_mail,provisional_pass)
    return send_message(provisional_pass,user_mail) if count_profile!=0 else False

