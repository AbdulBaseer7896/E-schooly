import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector


class user_model():
    engine = None

    def __init__(self):
        try:
            db_connection = os.environ.get('iqra_db_connection')
            print(f"db_connection: {db_connection}")
            self.engine = create_engine(db_connection, connect_args={
                "ssl": {
                    "ssl_ca": "/etc/ssl/cert.pem"
                }
            })
            print("connection build successfully")
        except:
            print("not work")

    def user_login_model(self, data):
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM user_login_table WHERE user_name = '{data['email_login']}' AND password = '{data['password_login']}' AND user_type = '{data['login-val']}';")
            user = conn.execute(query).fetchall()
        if user:
            print(data['login-val'])
            return True
        else:
            print(data['login-val'])
            return False