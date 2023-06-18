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
    
    def take_teacher_profile_data(self , data):
        print("THis  jsodj iasj if88 80u09 0 = " , data)
        with self.engine.connect() as conn:
            try:
                try:
                    query1 = text(f"SELECT * FROM  teacher_information WHERE name = '{data[0][0]}';")
                    result = conn.execute(query1).fetchall()
                except:
                    query1 = text(f"SELECT * FROM  teacher_information WHERE name = '{data['email_login']}';")
                    result = conn.execute(query1).fetchall()               
            except:
                query1 = text(f"SELECT * FROM  teacher_information WHERE name = '{data['teacher_mail']}';")
                result = conn.execute(query1).fetchall()
                
            if result:
                return result
            else:
                return render_template('login.html')
            
    def take_teacher_class_and_period_data(self , student_marks):
        with self.engine.connect() as conn:
            try:
                try:
                    query1 = text(f"SELECT DISTINCT * FROM  teacher_class_period WHERE teacher_name = '{student_marks['email_login']}';")
                    result = conn.execute(query1).fetchall()
                except:
                    query1 = text(f"SELECT DISTINCT * FROM  teacher_class_period WHERE teacher_name = '{student_marks[0][0]}';")
                    result = conn.execute(query1).fetchall()  
                    print("This is the result of teacher class period = " ,result)             
            except:
                    query1 = text(f"SELECT DISTINCT * FROM  teacher_class_period WHERE teacher_name = '{student_marks['teacher_mail']}';")
                    result = conn.execute(query1).fetchall()
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
            # query1 = text(f"Insert Into teacher_class_period Values( '{student_marks['book_name']}', chapter_name = '{student_marks['chapter_name']}', book_page_number = '{student_marks['book_page']}', dairy_date = '{student_marks['dairy_date']}', video_link = '{student_marks['video_link']}', helping_notes = '{image_path}', dairy_details = '{student_marks['dairy_details']}' ) WHERE (teacher_name = '{student_marks['teacher_mail']}' AND period_name = '{student_marks['period_name']}' AND  class_name = '{student_marks['class_name']}' );")
            query1 = text(f"INSERT INTO teacher_class_period ( teacher_name, class_name, period_name, bookname, chapter_name, book_page_number, dairy_date, video_link, helping_notes, dairy_details) VALUES ('{student_marks['teacher_mail']}', '{student_marks['class_name']}' , '{student_marks['period_name']}' , '{student_marks['book_name']}' , '{student_marks['chapter_name']}' , '{student_marks['book_page']}' , '{student_marks['dairy_date']}' , '{student_marks['video_link']}' , '{image_path}' , '{student_marks['dairy_details']}') ;")
            conn.execute(query1)
            # return flash("you dairy is send successfullu")
            
            
            
    def class_student_name_for_attendance(self  , student_marks ):
        print("This isj ijawig j  = = " , student_marks)
        with self.engine.connect() as conn:
            try:
                try:
                    query2 = text(f"SELECT class FROM teacher_information where name = '{student_marks[0][0]}';")
                    class_name = conn.execute(query2).fetchall() 
                except:
                    query1 = text(f"SELECT class FROM teacher_information where name = '{student_marks['email_login']}';")
                    class_name = conn.execute(query1).fetchall()
            except:
                    query1 = text(f"SELECT class FROM teacher_information where name = '{student_marks['teacher_mail']}';")
                    class_name = conn.execute(query1).fetchall()
            
            query3 = text(f"SELECT b_form_name , name , student_roll_number , class FROM student_information WHERE class = '{class_name[0][0]}'")
            student_name = conn.execute(query3).fetchall()
            if student_name:
                print('These are student name ,' , student_name)
                return student_name
            else:
                print("There are no student")
                flash(("There is no student in you class Kinldy contact with Admin !!!" , 'no_student_in_teacher_attandance'))
                return False
            
            
    def mark_student_attandance(self , student_marks):
        with self.engine.connect() as conn:
            print("THis is class data id i  = = =  = 444 = = " , student_marks)
            for i in range(0 , len(student_marks) ):
                if student_marks[i][3] == '1':
                    query1 = text(f"UPDATE student_information SET student_attendance = student_attendance + '1'  where name = '{student_marks[i][0]}';")
                    conn.execute(query1)
                    
            query2 = text(f"SELECT * from total_attendance where class = '{student_marks[0][1]}'; ")
            check = conn.execute(query2).fetchall()
            print("The class = " , student_marks[0][1])
            print("This is cheek = " , check)
                    
            if check:
                print("Thisi makrj  fkdasjf kojasdo fjoid  = =   =  =" , student_marks[0][1])
                query3 = text(f"UPDATE total_attendance SET total_student_attendance = total_student_attendance + '1'  where class = '{student_marks[0][1]}';")
                conn.execute(query3)
                print("Its run")
            else:
                query4 =  text(f"INSERT INTO total_attendance(class, total_student_attendance) VALUES ('{student_marks[i][1]}' , '1');")
                conn.execute(query4)
                print("This is except is run")
        
        print("the student attandace mark")
                    
                    
    def teacher_attandance(self , student_marks):
        with self.engine.connect() as conn:
            query2 = text(f"SELECT total_teacher_attendance FROM  total_attendance WHERE teacher = 'teacher';")
            total = conn.execute(query2).fetchall() 
            try:
                expression = f"((({total[0][0]} - {student_marks[0][16]})  / {total[0][0]})  * 100)"
                perstange = round(eval(expression) , 2)
            except:
                perstange = 0
                
            print("This is the attandane  of the teacher = " , perstange)
            return perstange
        
    
    def take_notification_details(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * FROM  teacher_notification;")
            total = conn.execute(query1).fetchall() 
        
        if total:
            return total
        else:
            print("NO notification is found")
            return False
        
    
        
        
            
    def take_teacher_class_form_db(self , student_marks):
        print("rijfi jsiadjfisjd ifjsdio j     = " , student_marks)
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
        print("data iaj si jioasj oasjo jf os" , data)
        with self.engine.connect() as conn:
            query1 = text(f"SELECT COUNT(*) FROM student_notification where class_name = '{data['teacher_class']}';")
            total_rows = conn.execute(query1).fetchall()
            print("This is toajf ajsdifjas " , total_rows)
            if total_rows[0][0] > 11:
                query2 = text(f"DELETE FROM student_notification WHERE notification_date = ( SELECT MIN(notification_date)   FROM (SELECT notification_date   FROM student_notification   WHERE class_name = '{data['teacher_class']}'    ORDER BY notification_date     LIMIT 1   ) AS subquery ) AND class_name = '{data['teacher_class']}';")
                total_rows = conn.execute(query2)
                
            print("The student_marks is = " ,data['titles'])
            query3 = text(f"INSERT INTO student_notification VALUES ('{data['titles']}' , '{data['date']}' , '{data['teacher_class']}' , '{data['details']}' , '{file_path}');")
            conn.execute(query3)
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
                        if student_marks[0] != None and student_marks[1] != None:
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
     
     
     
     
     
    def take_teacher_dariy_for_db_for_delete(self , data):
        with self.engine.connect() as conn:
            print("The data is === " , data)
            try:
                try:
                    query1 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = '{data['email_login']}' ORDER BY dairy_date DESC;")
                    dairy = conn.execute(query1).fetchall() 
                    print("This is the dairy of the student = " ,dairy)
                
                except:
                    query2 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = '{data[0][0]}' ORDER BY dairy_date DESC;")
                    dairy = conn.execute(query2).fetchall() 
                    print("This is the dairy of the student = " ,dairy)
                    print('Thisi sfjaisdjgi a= ' , data)
            except:
                    query1 = text(f"SELECT * FROM  teacher_class_period WHERE teacher_name = '{data['teacher_mail']}' ORDER BY dairy_date DESC;")
                    dairy = conn.execute(query1).fetchall() 
                    print("This is the dairy of the student = " ,dairy)
            return dairy

            
    def delete_dariy_for_db_which_teacher_select(self , data):
        with self.engine.connect() as conn:
            print("The data is === " , data)
            query1 = text(f"DELETE FROM teacher_class_period WHERE teacher_name = '{data[0]}' AND class_name = '{data[1]}' AND  period_name = '{data[2]}' AND bookname = '{data[3]}' And chapter_name = '{data[4]}' And book_page_number = '{data[5]}'  And video_link = '{data[7]}' And helping_notes = '{data[8]}' And dairy_details = '{data[9]}' ;")
            cheek = conn.execute(query1)
            print("The dariy is delete for file")
            print(data[8])
            if data[8] != "":
                os.remove(f"static/{data[8]}")
            print("The file is remove for files")
            print("This is cheek" , cheek)
            return cheek
            
            
    def take_teacher_notification_of_class_for_db_for_delete(self , data):
        print("Now the data is is is = " ,data)
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT class FROM teacher_information where name = '{data['email_login']}';")
                class_name = conn.execute(query1).fetchall()            
                print("The class name = ," , class_name[0][0])
            except:
                query1 = text(f"SELECT class FROM teacher_information where name = '{data[0][0]}';")
                class_name = conn.execute(query1).fetchall()            
                print("The class name = ," , class_name[0][0])
                
            query1 = text(f"SELECT * FROM student_notification where class_name = '{class_name[0][0]}' ORDER BY notification_date DESC;")
            notification = conn.execute(query1).fetchall() 
            print("This is student notification of class = = " , notification)
            if notification:
                formatted_notification = []
                for entry in notification:
                    title = entry[0]
                    notification_date = entry[1].strftime('%Y-%m-%d')
                    class_name = entry[2]
                    datails = entry[3]
                    document_path = entry[4]
                    formatted_entry = (title, notification_date, class_name , datails, document_path)
                    formatted_notification.append(formatted_entry)
                print("This is the dairy of the student = ", formatted_notification)
                return formatted_notification
            else:
                return False
            
            
            
            
            
            
            
            
    def delete_selected_notification_form_data(self , data):
        print("The data i s0485  = = ", data)
        with self.engine.connect() as conn:
            print("The data is === " , data)

            query2 = text(f"DELETE FROM student_notification WHERE title = '{data[0]}' AND notification_date = '{data[1]}' AND  datails = '{data[3]}' AND (document_path = '{data[4]}' OR document_path IS NULL) and class_name = '{data[2]}';")
            cheek = conn.execute(query2)
            
            print("The dariy is delete for file")
            print(data[4])
            if data[4] == None or data[4] == "":
                return cheek  
            else:
                os.remove(f"static/{data[4]}")
