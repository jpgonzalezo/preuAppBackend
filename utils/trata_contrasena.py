import random
import string
from flask import current_app
from flask_mail import Message
from mail import mail


def send_message(codigo, email):
    msg = Message('AVISO, CAMBIO DE CONTRASENA SOLICITADO', sender = current_app.config['MAIL_USERNAME'], recipients = [email])
    msg.body = "Hola, tu codigo de recuperacion es: " + codigo + " ingresa al siguiente link para acceder al cambio http://localhost:4200/inicio/cambiaPass"
    mail.send(msg)
    return "Message sent!"


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters)
        for i in range(length))
    # print random string
    return(result_str)

def validate_code_provisional(admin, alumno, apoderado, profesor):
    list_codes= []
    count_profile = 0
    if (admin != None):
        list_codes.append(admin.password_provisoria)
        count_profile += 1

    if (alumno != None):
        list_codes.append(alumno.password_provisoria)
        count_profile += 1

    if (apoderado != None):
        list_codes.append(apoderado.password_provisoria)
        count_profile += 1

    if (profesor != None):
        list_codes.append(profesor.password_provisoria)
        count_profile += 1
    lista = [count_profile,list_codes]
    return lista

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


def change_pass(new_password, admin, alumno, apoderado, profesor):
    if (admin != None):
        admin.encrypt_password(new_password)
        admin.save()
    if (alumno != None):
        alumno.encrypt_password(new_password)
        alumno.save()
    if (apoderado != None):
        apoderado.encrypt_password(new_password)
        apoderado.save()
    if (profesor != None):
        profesor.encrypt_password(new_password)
        profesor.save()
    return "hecho"

