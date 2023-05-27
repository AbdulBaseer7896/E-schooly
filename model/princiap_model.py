import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector


class principal_models():
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


    def stored_teacher_period_data(self , data):
        with self.engine.connect() as conn:
            print("This is period [" ,  data['period1'] , "]")
            if data['teacher_name'] != "":
                for i in range(1 , 9):
                    if data[f'class{i}'] != "free" and data[f'period{i}'] != "free":
                        print("The class = " , data[f'class{i}'] , "The period is = " , data[f'period{i}'])
                        
                        # query1 = text(f"INSERT INTO teacher_class_period (teacher_name, class_name, period_name) VALUES('{data['teacher_name']}', '{data[f'class{i}']}', ' data[f'period{i}');")

                        query = text(f"INSERT INTO teacher_class_period (teacher_name, class_name, period_name) "
                        f"VALUES ('{data['teacher_name']}', '{data[f'class{i}']}', '{data[f'period{i}']}') "
                        f"ON DUPLICATE KEY UPDATE "
                        f"teacher_name = '{data['teacher_name']}' , "
                        f"class_name = '{data[f'class{i}']}', "
                        f"period_name = '{data[f'period{i}']}'")
                        user = conn.execute(query)
            else:
                print("Enter the name of Teacher")
                return render_template('principal_URLs/teacher_periods.html')
            
    def teacher_names(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT name , cnic_name , teacher_id from teacher_information;")
            cheek = conn.execute(query1).fetchall()
            print("This is teacher names = " , cheek)
            return cheek