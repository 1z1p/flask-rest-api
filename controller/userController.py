from flask import request, jsonify
from db.db import connect
import pymysql
import jwt
import datetime
from config import config
import hashlib
import os

if(connect):
    print('Connect database success')
    
def signup():
    req = request.get_json()
    try:
        if req['email'] == "" or req['password'] == "" or req['phone'] == "" or req['name'] == "":
            return jsonify({"Error": "Заполните данные"})
        else:
            with connect.cursor() as base_query:
                base_query.execute("SELECT `email` FROM `users` WHERE `email` = '" + req['email'] + "'")
                rows = base_query.fetchall()

                if str(rows) == "()":
                    sql = "INSERT INTO `users`(`email`, `password`, `phone`, `name`) VALUES (%s,%s,%s,%s)"

                    password = req['password'].encode()
                    salt = 'sole'.encode()
                    dk = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
                    password_hash = dk.hex()

                    base_query.execute(sql, (req['email'], password_hash, req['phone'], req['name'])) 
                    connect.commit()
                    return jsonify({"Success": "Регистрация прошла успешно"})
                else:
                    return jsonify({"Error": "Пользователь с таким E-mail существует"})   
    except:
        return jsonify({"Error": "Данные JSON не подходят"})
        
def signin():
    req = request.get_json()
    try:
        if req['email'] == "" or req['password'] == "":
            return jsonify({"Error": "Заполните данные"})
        else:
            with connect.cursor() as base_query:
                base_query.execute("SELECT `email` FROM `users` WHERE `email` = '" + req['email'] + "'")
                rows = base_query.fetchall()

                if str(rows) == "()":
                    return jsonify({"Error": "Пользователь с таким E-mail не существует"})
                else:
                    try:
                        password = req['password'].encode()
                        salt = 'sole'.encode()
                        dk = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
                        password_hash = dk.hex()

                        base_query.execute("SELECT * FROM users WHERE `email` = '"+ req['email'] +"' and `password` = '"+ password_hash +"'") 
                        rows = base_query.fetchall()
                        if password_hash == rows[0][2]:    
                            json_data = {
                                "email": req['email'],
                                "password": password_hash,
                                "phone": rows[0][3],
                                "name": rows[0][4],
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)
                            }
                            encode_data = jwt.encode(payload=json_data, key=config["secret"], algorithm="HS256")
                            return jsonify({"token": encode_data})
                    except:
                        return jsonify({"Error": "Пароль не верный"})
                        
    except:
        return jsonify({"Error": "Данные JSON не подходят"})

def infoUserToken():
    try:
        token = request.headers['Authorization']
        decode_data = jwt.decode(jwt=token, key=config["secret"], algorithms="HS256")
        return jsonify({"data": decode_data})
    except Exception as e:
        message = f"Token не действителен -- > {e}"
        return jsonify({"Error": message})


