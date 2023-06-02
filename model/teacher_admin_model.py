import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector
from datetime import datetime


class teacher_admin_model():
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
    
    def teacher_name_for_attendance(self , data):
        with self.engine.connect() as conn:            
            query2 = text(f"SELECT cnic_name , name , teacher_id , cnic_number FROM teacher_information ;")
            teacher_name = conn.execute(query2).fetchall()
            if teacher_name:
                print('These are teacher name ,' , teacher_name)
                return teacher_name
            else:
                print("There are no Teacher")
                return "No teacher found :"
            
            
    def mark_teacher_attandance(self , data):
        with self.engine.connect() as conn:
            for i in range(0 , len(data) ):
                if data[i][3] == '1':
                    query1 = text(f"UPDATE teacher_information SET teacher_attendance = teacher_attendance + '1'  where name = '{data[i][0]}';")
                    conn.execute(query1)
                    
            query2 = text(f"UPDATE total_attendance SET total_teacher_attendance = total_teacher_attendance + '1' where teacher = teacher")
            conn.execute(query2)
            print("Its run")
        print("the student attandace mark")
        
        
    def send_notification_of_db(self , data , file_path):
        with self.engine.connect() as conn:
            print("The data is = " ,data['titles'])
            if data['titles'] != "":
                query1 = text(f"INSERT INTO teacher_notification VALUES ('{data['titles']}' , '{data['date']}' , '{data['details']}' , '{file_path}' );")
                conn.execute(query1)
                return True
            return False
        
        
    def stored_notification_in_file_and_send_path_in_db(self , file , folder_name):
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
        
        
    def take_techer_admin_notification_for_db_for_delete(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * FROM teacher_notification ORDER BY notification_date DESC;")
            notification = conn.execute(query1).fetchall() 
            if notification:
                print("This is the dairy of the student = ", notification)
                return notification
            else:
                return False
            
            
    def delete_selected_notification_form_data(self , data):
        print("The data i s0485  = = ", data)
        with self.engine.connect() as conn:
            print("The data is === " , data)
            query1 = text(f"DELETE FROM teacher_notification WHERE title = '{data[0]}' AND notification_date = '{data[1]}' AND  details = '{data[2]}' AND (document_path = '{data[3]}' OR document_path IS NULL);")
            cheek = conn.execute(query1)
            
            print("The dariy is delete for file")
            print(data[3])
            if data[3] != None:
                os.remove(f"static/{data[3]}")
            return cheek

