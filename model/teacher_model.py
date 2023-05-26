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
            
            
            
    def class_student_name_for_attendance(self  , data):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT class FROM teacher_information where name = '{data['email_login']}';")
            class_name = conn.execute(query1).fetchall()
            
            
            query2 = text(f"SELECT b_form_name , name , student_roll_number , class FROM student_information WHERE class = 'Class {class_name[0][0]}'")
            student_name = conn.execute(query2).fetchall()
            if student_name:
                print('These are student name ,' , student_name)
                return student_name
            else:
                print("There are no student")
                return "No class student found in this class"
            
    def mark_student_attandance(self , data):
        with self.engine.connect() as conn:
            for i in range(0 , len(data) ):
                if data[i][3] == '1':
                    query1 = text(f"UPDATE student_information SET student_attendance = student_attendance + '1'  where name = '{data[i][0]}';")
                    conn.execute(query1)
                    
            query2 = text(f"SELECT * from total_student_attandance where class = '{data[0][1]}'; ")
            check = conn.execute(query2).fetchall()
            print("The class = " , data[0][1])
            print("This is cheek = " , check)
                    
            if check:
                query3 = text(f"UPDATE total_student_attandance SET total_attendance = total_attendance + '1'  where class = '{data[i][1]}';")
                conn.execute(query3)
                print("Its run")
            else:
                query4 =  text(f"INSERT INTO total_student_attandance(class, total_attendance) VALUES ('{data[i][1]}' , '{data[i][3]}');")
                conn.execute(query4)
                print("This is except is run")
        
        print("the student attandace mark")
                    
                    
    def teacher_attandance(self , data):
        with self.engine.connect() as conn:
            query2 = text(f"SELECT total_teacher_attendance FROM  total_attendance WHERE teacher = 'teacher';")
            total = conn.execute(query2).fetchall() 
                
                # total_present =  
            expression = f"((({total[0][0]} - {data[0][16]})  / {total[0][0]})  * 100)"
            perstange = round(eval(expression) , 2)
                
            print("This is the attandane  of the teacher = " , perstange)
            return perstange
        
        print("The perstange is not found is not found")
        return render_template('login.html')
    
    def take_notification_details(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * FROM  teacher_notification;")
            total = conn.execute(query1).fetchall() 
        
        if total:
            return total
        else:
            print("NO notification is found")
            return "no notification is found"
        
        
            
            
            
        
    