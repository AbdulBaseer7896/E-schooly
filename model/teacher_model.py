import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector


class teacher_model():
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
    
    def take_teacher_profile_data(self , data):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT * FROM  teacher_information WHERE name = '{data['email_login']}';")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT * FROM  teacher_information WHERE name = '{data[0][0]}';")
                result = conn.execute(query1).fetchall()               
            if result:
                return result
            else:
                return render_template('login.html')
            
    def take_teacher_class_and_period_data(self , data):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = '{data['email_login']}';")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = '{data[0][0]}';")
                result = conn.execute(query1).fetchall()  
                print("This is the result of teacher class period = " ,result)             
            if result:
                return result
            else:
                return render_template('login.html')
            
            
    def cross_cheed_class_period(self , data ):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = '{data['teacher_mail']}' ANd class_name = '{data['teacher_class']}' AND period_name = '{data['teacher_period']}' ;")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = {data[0][0]} and  class_name = {data[0][1]} and period_name = {data[0][2]};")
                result = conn.execute(query1).fetchall()   
                print("This is the result of teacher class period = " ,result)             
            if result:
                print("The teacher can apploat the dairy")
                return True
            else:
                print("teacher can not upload the dairy")
                return False
            
            
    def send_dairy(self , data):
        with self.engine.connect() as conn:
            query1 = text(f"UPDATE teacher_class_period SET bookname = '{data['book_name']}', chapter_name = '{data['chapter_name']}', book_page_number = '{data['book_page']}', dairy_date = '{data['dairy_date']}', video_link = '{data['video_link']}', helping_notes = '{data['helping_notes']}', dairy_details = '{data['dairy_details']}' WHERE (teacher_name = '{data['teacher_mail']}' AND period_name = '{data['period_name']}' AND  class_name = '{data['class_name']}' );")
            conn.execute(query1)
            # return flash("you dairy is send successfullu")
            
            
        
        
            
            
            
        
    