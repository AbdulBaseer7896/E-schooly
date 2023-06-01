import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector
from datetime import datetime


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
    
    def take_teacher_profile_data(self , student_marks):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT * FROM  teacher_information WHERE name = '{student_marks['email_login']}';")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT * FROM  teacher_information WHERE name = '{student_marks[0][0]}';")
                result = conn.execute(query1).fetchall()               
            if result:
                return result
            else:
                return render_template('login.html')
            
    def take_teacher_class_and_period_data(self , student_marks):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = '{student_marks['email_login']}';")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = '{student_marks[0][0]}';")
                result = conn.execute(query1).fetchall()  
                print("This is the result of teacher class period = " ,result)             
            if result:
                return result
            else:
                return render_template('login.html')
            
            
    def cross_cheed_class_period(self , student_marks ):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = '{student_marks['teacher_mail']}' ANd class_name = '{student_marks['teacher_class']}' AND period_name = '{student_marks['teacher_period']}' ;")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = {student_marks[0][0]} and  class_name = {student_marks[0][1]} and period_name = {student_marks[0][2]};")
                result = conn.execute(query1).fetchall()   
                print("This is the result of teacher class period = " ,result)             
            if result:
                print("The teacher can apploat the dairy")
                return True
            else:
                print("teacher can not upload the dairy")
                return False
            
            
    def send_dairy(self , student_marks , image_path):
        with self.engine.connect() as conn:
            query1 = text(f"UPDATE teacher_class_period SET bookname = '{student_marks['book_name']}', chapter_name = '{student_marks['chapter_name']}', book_page_number = '{student_marks['book_page']}', dairy_date = '{student_marks['dairy_date']}', video_link = '{student_marks['video_link']}', helping_notes = '{image_path}', dairy_details = '{student_marks['dairy_details']}' WHERE (teacher_name = '{student_marks['teacher_mail']}' AND period_name = '{student_marks['period_name']}' AND  class_name = '{student_marks['class_name']}' );")
            conn.execute(query1)
            # return flash("you dairy is send successfullu")
            
            
            
    def class_student_name_for_attendance(self  , student_marks):
        with self.engine.connect() as conn:
            try:
                query2 = text(f"SELECT class FROM teacher_information where name = '{student_marks[0][0]}';")
                class_name = conn.execute(query2).fetchall() 
            except:
                query1 = text(f"SELECT class FROM teacher_information where name = '{student_marks['email_login']}';")
                class_name = conn.execute(query1).fetchall()
                             
            
            query3 = text(f"SELECT b_form_name , name , student_roll_number , class FROM student_information WHERE class = '{class_name[0][0]}'")
            student_name = conn.execute(query3).fetchall()
            if student_name:
                print('These are student name ,' , student_name)
                return student_name
            else:
                print("There are no student")
                return False
            
    def mark_student_attandance(self , student_marks):
        with self.engine.connect() as conn:
            for i in range(0 , len(student_marks) ):
                if student_marks[i][3] == '1':
                    query1 = text(f"UPDATE student_information SET student_attendance = student_attendance + '1'  where name = '{student_marks[i][0]}';")
                    conn.execute(query1)
                    
            query2 = text(f"SELECT * from total_attendance where class = '{student_marks[0][1]}'; ")
            check = conn.execute(query2).fetchall()
            print("The class = " , student_marks[0][1])
            print("This is cheek = " , check)
                    
            if check:
                query3 = text(f"UPDATE total_attendance SET total_student_attendance = total_student_attendance + '1'  where class = '{student_marks[i][1]}';")
                conn.execute(query3)
                print("Its run")
            else:
                query4 =  text(f"INSERT INTO total_attendance(class, total_student_attendance) VALUES ('{student_marks[i][1]}' , '{student_marks[i][3]}');")
                conn.execute(query4)
                print("This is except is run")
        
        print("the student attandace mark")
                    
                    
    def teacher_attandance(self , student_marks):
        with self.engine.connect() as conn:
            query2 = text(f"SELECT total_teacher_attendance FROM  total_attendance WHERE teacher = 'teacher';")
            total = conn.execute(query2).fetchall() 
                
                # total_present =  
            expression = f"((({total[0][0]} - {student_marks[0][16]})  / {total[0][0]})  * 100)"
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
        
    
        
        
            
    def take_teacher_class_form_db(self , student_marks):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT class FROM  teacher_information WHERE name = '{student_marks[0][0]}';")
                result = conn.execute(query1).fetchall() 
                if result:
                    return result

            except:
                query2 = text(f"SELECT class FROM  teacher_information WHERE name = '{student_marks['email_login']}';")
                result = conn.execute(query2).fetchall()
                print("This is alos result = " , result)
                if result:
                    return result
        
        return   print('The teacher has no class')
        
        
        
    def send_student_notification_to_db(self , data , file_path):
        with self.engine.connect() as conn:
            print("The student_marks is = " ,data['titles'])
            query1 = text(f"INSERT INTO student_notification VALUES ('{data['titles']}' , '{data['date']}' , '{data['teacher_class']}' , '{data['details']}' , '{file_path}');")
            conn.execute(query1)
            print("The notification is send now")
            
            
    def take_class_student_id_form_db(self , student_marks):
        with self.engine.connect() as conn:
            print("This is = " , student_marks[0][0])
            try:
                query1 = text(f"SELECT name , b_form_name , student_roll_number FROM  student_information WHERE class = '{student_marks[0][0]}';")
                result = conn.execute(query1).fetchall() 
                if result:
                    return result

            except:
                query2 = text(f"SELECT name , b_form_name , student_roll_number FROM  student_information class = '{student_marks['teacher_class']}';")
                result = conn.execute(query2).fetchall()
                print("This is alos result = " , result)
                if result:
                    return result
        
        return   print('The teacher has no class')
    
    
    def take_class_subject_from_db(self , student_marks):
        with self.engine.connect() as conn:
            print("This is = " , student_marks[0][0])
            try:
                query1 = text(f"SELECT DISTINCT period_name FROM  teacher_class_period WHERE class_name = '{student_marks[0][0]}';")
                result = conn.execute(query1).fetchall() 
                if result:
                    return result

            except:
                query2 = text(f"SELECT DISTINCT period_name FROM  teacher_class_period class_name = '{student_marks['teacher_class']}';")
                result = conn.execute(query2).fetchall()
                print("This is alos result = " , result)
                if result:
                    return result
        
        return   print('The teacher subject')
            
            
            
        


    def send_student_marks_of_db(self , student_marks , result_type_data):
        print("This is marks of student = " , student_marks)
        print("This is result type data = = " , result_type_data)
        with self.engine.connect() as conn:
            try:
                if {result_type_data[0]} == "" and {result_type_data[2]} == "" and {result_type_data[1]} == "" and {student_marks[i][5]} == "":
                    print("You will not fill the result_type or subject or date or total marks")
                else:
                    for i in range(0 , len(student_marks)):
                            query1 = text(f"INSERT INTO result_student_subject_marks (b_form_name, student_email, roll_number, markes, subject, class , result_type ,total_marks ,result_date) VALUES ('{student_marks[i][3]}', '{student_marks[i][0]}', '{student_marks[i][1]}', {student_marks[i][2]} , '{student_marks[i][5]}' , '{student_marks[i][4]}' , '{result_type_data[0]}' , '{result_type_data[2]}' ,'{result_type_data[1]}');")
                            conn.execute(query1)
                    print("Result and subject student_marks insert in student_marksbase")
                    return True
            except:
                print("The student_marks is not send in student_marksbase")
                return False
            
            
            
    def stored_dariy_in_file_and_send_path_in_db(self , file , folder_name):
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
