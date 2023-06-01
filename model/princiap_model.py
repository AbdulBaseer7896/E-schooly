import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector
from datetime import datetime


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
        
        
    def make_class_teacher(self , data):
        with self.engine.connect() as conn:
            query1 = text(f"UPDATE teacher_information SET class = '{data['teacher_class']}' WHERE name = '{data['teacher_name']}' ")
            conn.execute(query1)
            print("The teacher class is updated")
        
    def send_principal_notification_of_db(self , data , file_path):
        with self.engine.connect() as conn:
            print("The data is = " ,data['titles'])
            
            if data['titles'] != "" and data['target_audience'] == 'teacher':
                query1 = text(f"INSERT INTO teacher_notification VALUES ('{data['titles']}' , '{data['date']}' , '{data['details']}' , '{file_path}');")
                conn.execute(query1)
                return True
            elif  data['titles'] != "" and data['target_audience'] == 'student':
                query2 = text(f"INSERT INTO student_notification VALUES ('{data['titles']}' , '{data['date']}'  , 'school' , '{data['details']}' , {file_path}' );")
                conn.execute(query2)
                return True
            elif  data['titles'] != "" and data['target_audience'] == 'both':         
                query3 = text(f"INSERT INTO teacher_notification VALUES ('{data['titles']}' , '{data['date']}' , '{data['details']}' , '{file_path}' );")
                conn.execute(query3)
                
                query4 = text(f"INSERT INTO student_notification VALUES ('{data['titles']}' , '{data['date']}'  , 'school' , '{data['details']}' , '{file_path}');")
                conn.execute(query4)
                return True
            
            return False
        
        
    def stored_notification_and_send_path_in_db(self , file , folder_name):
        if file is not None:
            new_filename = str(datetime.now().timestamp()).replace(".", "")  # Generating unique name for the file
            # Spliting ORIGINAL filename to seperate extenstion
            split_filename = file.filename.split(".")
            # Canlculating last index of the list got by splitting the filname
            ext_pos = len(split_filename)-1
            # Using last index to get the file extension
            ext = split_filename[ext_pos]
            img_db_path = str(f"documents/{folder_name}/{new_filename}.{ext}")
            print("The type of path  = ", type(img_db_path))
            file.save(f"static/documents/{folder_name}/{new_filename}.{ext}")
            print("File uploaded successfully")
            return img_db_path
