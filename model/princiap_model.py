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
                        query1 = text(f"Select * from teacher_class_period where teacher_name = '{data['teacher_name']}' AND class_name = '{data[f'class{i}']}' AND period_name = '{data[f'period{i}']}';")
                        cheeK_if_already = conn.execute(query1).fetchall() 
                        if cheeK_if_already:
                            print("ITs alread present in data base")
                        else:
                            query2 = text(f"Select teacher_name from teacher_class_period where  class_name = '{data[f'class{i}']}' AND period_name = '{data[f'period{i}']}';")
                            cheeK_if_already_any_one_teach = conn.execute(query2).fetchall() 
                            print("This is cheek if alredf sdfjsdf = " , cheeK_if_already_any_one_teach)
                            if cheeK_if_already_any_one_teach:
                                query3 = text(f"UPDATE teacher_class_period SET teacher_name = '{data['teacher_name']}'   WHERE teacher_name = '{cheeK_if_already_any_one_teach[0][0]}' AND class_name = '{data[f'class{i}']}' AND period_name = '{data[f'period{i}']}';")
                                conn.execute(query3)
                            else:
                                query4 = text(f"INSERT INTO teacher_class_period (teacher_name, class_name, period_name) VALUES('{data['teacher_name']}', '{data[f'class{i}']}', '{data[f'period{i}']}');")
                                conn.execute(query4)
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
            print("This is data = " , data)
            print("This is the idifj s = =  =" , data['teacher_class'])
            if data['teacher_class'] != "Helper":
                query1 = text(f"select class from teacher_information where class = '{data['teacher_class']}';")
                cheek = conn.execute(query1).fetchall()
                if cheek:          
                    query2 = text(f"UPDATE teacher_information SET class = 'helper' WHERE class = '{data['teacher_class']}' ;" )  
                    conn.execute(query2)
                query1 = text(f"UPDATE teacher_information SET class = '{data['teacher_class']}' WHERE name = '{data['teacher_name']}'; ")
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


    def take_principal_notification_for_db_for_delete(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT 'student_notification' AS source, title, notification_date, datails , document_path FROM student_notification UNION ALL SELECT 'teacher_notification' AS source, title, notification_date, details , document_path FROM teacher_notification ORDER BY notification_date DESC;")
            notification = conn.execute(query1).fetchall() 
            if notification:
                formatted_notification = []
                for entry in notification:
                    source = entry[0]
                    title = entry[1]
                    notification_date = entry[2].strftime('%Y-%m-%d')
                    details = entry[3]
                    document_path = entry[4]
                    formatted_entry = (source, title, notification_date, details, document_path)
                    formatted_notification.append(formatted_entry)
                print("This is the dairy of the student = ", notification)
                return formatted_notification
            else:
                return False
            
            
    def delete_selected_notification_form_data(self , data):
        print("The data i s0485  = = ", data)
        with self.engine.connect() as conn:
            print("The data is === " , data)
            query1 = text(f"DELETE FROM teacher_notification WHERE title = '{data[1]}' AND notification_date = '{data[2]}' AND  details = '{data[3]}' AND (document_path = '{data[4]}' OR document_path IS NULL);")
            cheek = conn.execute(query1)

            query2 = text(f"DELETE FROM student_notification WHERE title = '{data[1]}' AND notification_date = '{data[2]}' AND  datails = '{data[3]}' AND (document_path = '{data[4]}' OR document_path IS NULL);")
            cheek = conn.execute(query2)
            
            print("The dariy is delete for file")
            print(data[4])
            if data[4] != "":
                os.remove(f"static/{data[4]}")
            return cheek
        
        

    def take_teacher_period_data_for_db(self):
        print("The data   = = infoaosig hoa")
        with self.engine.connect() as conn:
            query1 = text(f"SELECT class_name ,  teacher_name , period_name FROM  teacher_class_period order by class_name desc;")
            period_data = conn.execute(query1).fetchall() 
            print("This is very important data  = = = =  = " , period_data)
            return period_data
        
    def take_class_teacher_data_for_db(self):
        print("This is class teacher")
        with self.engine.connect() as conn:
            query1 = text(f"SELECT  class , cnic_name , name  FROM  teacher_information ORDER BY class ASC;")
            class_teacher_name = conn.execute(query1).fetchall() 
            if class_teacher_name:
                print("This is very important data  = = = =  = " , class_teacher_name)
                return class_teacher_name
            else:
                print("Ther is not teacher in the data base")
                return False
        
        

    def search_student_admission_data_for_principal(self, data):
        print("The is search student admission data")
        with self.engine.connect() as conn:
            try:
                query = text(f"SELECT * FROM student_information WHERE name = '{data['email_search']}' OR form_b = '{data['b_from_search']}' OR student_registration_number = '{data['student_registration_number']}';")
                user = conn.execute(query).fetchall()
            except:
                query = text(f"SELECT * FROM student_information WHERE name = '{data[0]}' OR form_b = '{data[1]}' OR student_registration_number = '{data[2]}';")
                user = conn.execute(query).fetchall()
            if user:
                print("the data in user is = ")
                print(user)
                return user
            else:
                return ""
                # return render_template('school_admin_URLs/school_admin_dashboard.html' , data = user)
                
                

    def take_student_result_data_for_principal(self , data):
        print("This is sj foiajsgoi jsogj aosjgo ja   = = = = " , data)
        with self.engine.connect() as conn:
            query1 = text(f"SELECT b_form_name, roll_number , student_email , result_type, subject, markes , total_marks , result_date  FROM result_student_subject_marks WHERE student_email = '{data}' ORDER BY result_type, result_date DESC;")
            result = conn.execute(query1).fetchall()
            return result


    def search_user_data_for_forger_password_by_principal(self , data):
        print("The is search  teacher data" , data)
        with self.engine.connect() as conn:
            if data['login-val'] == 'student':
                print("This is student")
                query = text(f"SELECT * FROM student_information WHERE name = '{data['email_search']}' OR form_b = '{data['b_from_search']}' OR student_registration_number = '{data['search_registration_number']}';")
                user = conn.execute(query).fetchall()
            elif data['login-val'] == 'teacher':
                print("This is teacher")
                query = text(f"SELECT * FROM teacher_information WHERE name = '{data['email_search']}' OR cnic_number = '{data['b_from_search']}' OR teacher_id = '{data['search_registration_number']}';")
                user = conn.execute(query).fetchall()
            elif data['login-val'] == 'teacher_admin':
                print("This is teacher admin")
                query = text(f"SELECT * FROM user_login_table WHERE user_name = '{data['email_search']}' OR user_type = 'teacher_admin';")
                user = conn.execute(query).fetchall()
                
            elif data['login-val'] == 'school_admin':
                print("This is principal")
                query = text(f"SELECT * FROM user_login_table WHERE user_name = '{data['email_search']}' OR user_type = 'school_admin';")
                user = conn.execute(query).fetchall()
            else:
                return False
            
            if user:
                print("the data in user is = ")
                print(user)
                return user
            else:
                return False
            
            
    def search_user_passwrod_by_principal(self , data):
        print("The data = d = = 99999 = " , data)
        print("The data = d = = 99999 = " , data[0][0])
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM user_login_table WHERE user_name = '{data[0][0]}';")
            user = conn.execute(query).fetchall()
            return user
        
        
    def take_teacher_attandance_for_db(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT cnic_name , name , whatapp_number , teacher_id , teacher_attendance  FROM teacher_information ORDER BY teacher_attendance DESC;")
            user = conn.execute(query).fetchall()
            return user
        
    
    def take_total_number_of_working_days_of_teacher(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT total_teacher_attendance  FROM total_attendance;")
            user = conn.execute(query).fetchall()
            return user
        
        
    
    def stored_school_images_and_send_path_in_db(self , file, folder_name):
        if file is not None:
            new_filename = str(datetime.now().timestamp()).replace(".", "")  # Generating unique name for the file
            # Spliting ORIGINAL filename to seperate extenstion
            split_filename = file.filename.split(".")
            # Canlculating last index of the list got by splitting the filname
            ext_pos = len(split_filename)-1
            # Using last index to get the file extension
            ext = split_filename[ext_pos]
            img_db_path = str(f"images/school_images/{folder_name}/{new_filename}.{ext}")
            print("The type of path  = ", type(img_db_path))
            file.save(f"static/images/school_images/{folder_name}/{new_filename}.{ext}")
            print("File uploaded successfully")
            return img_db_path


    def stored_school_image_path_to_db(self , data , image_path):
        print("THe dat is == = =" , data)
        print(image_path)
        with self.engine.connect() as conn:
            query = text(f"INSERT INTO school_event_images (image_category, target_area, image_file, posting_date) VALUES ('{data['image_category']}', '{data['target_area']}', '{image_path}', '{data['posting_date']}');")
            conn.execute(query)
            return True
        
    
    
    def get_gallery_images_for_principal_form_db(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM school_event_images WHERE target_area = 'Iqra_gallery' ORDER BY image_category;")
            user = conn.execute(query).fetchall()
            if user:
                return user
            else:
                return False
            
            
    def get_post_images_for_principal_form_db(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM school_event_images WHERE target_area = 'Iqra_posts' ORDER BY image_category;")
            user = conn.execute(query).fetchall()
            print("Tisi osdj fpijds pifjpisa fio = = = = " , user)
            if user:
                return user
            else:
                return False
            
    def delete_image_form_db_and_file(self , data):
        
        with self.engine.connect() as conn:
            query = text(f"DELETE FROM school_event_images WHERE image_file = '{data}';")
            conn.execute(query)
            
        print("The dariy is delete for file")
        print(data[3])
        if data != "":
            os.remove(f"static/{data}")
