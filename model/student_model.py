import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector


class student_model():
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
    
    def take_student_profile_data(self , data):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT * FROM  student_information WHERE name = '{data['email_login']}';")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT * FROM  student_information WHERE name = '{data[0][0]}';")
                result = conn.execute(query1).fetchall()               
            if result:
                return result
            else:
                return render_template('login.html')
    