import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector


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