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
                print("its also work")
            except:
                query1 = text(f"SELECT * FROM  student_information WHERE name = '{data[0][0]}';")
                result = conn.execute(query1).fetchall()
                print("its work")          
            if result:
                print("This is result of take student " , result)
                return result
            # else:
                # return render_template('login.html')
            
    def take_student_dairy_data(self , data):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT class FROM  student_information WHERE name = '{data['email_login']}';")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT class FROM  student_information WHERE name = '{data[0][0]}';")
                result = conn.execute(query1).fetchall()      
            if result:
                query2 = text(f"SELECT * FROM  teacher_class_period WHERE class_name = '{result[0][0]}';")
                dairy = conn.execute(query2).fetchall() 
                print("This is the dairy of the student = " ,dairy)
                return dairy
            else:
                print("The dairy is not found")
                return render_template('login.html')
            
    def attandance(self , data):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT class FROM  student_information WHERE name = '{data['email_login']}';")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT class FROM  student_information WHERE name = '{data[0][0]}';")
                result = conn.execute(query1).fetchall()      
            if result:
                query2 = text(f"SELECT total_student_attendance FROM  total_attandance WHERE class = '{result[0][0]}';")
                total = conn.execute(query2).fetchall() 
                
                # total_present =  
                expression = f"((({total[0][0]} - {data[0][19]})  / {total[0][0]})  * 100)"
                perstange = round(eval(expression) , 2)
                
                print("This is the dairy of the student = " , perstange)
                return perstange
            else:
                print("The perstange is not found is not found")
                return render_template('login.html')
        
              
    