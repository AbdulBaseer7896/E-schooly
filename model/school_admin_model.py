import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector
from datetime import datetime

class school_admin_models():
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

    def student_admission_data(self, data , image_path):
        with self.engine.connect() as conn:
                query1 = text(f"SELECT COUNT(*)  From student_information WHERE class = '{data['student_class']}';")
                count1 = conn.execute(query1).fetchall()

                query2 = text(f"SELECT COUNT(*)  From student_information;")
                count2 = conn.execute(query2).fetchall()
                
                email = f"{data['student_name']}-{count1[0][0]+1}-{count2[0][0]+1}-{data['student_class']}@iqra.edu"
                modified_email = email.replace("Class ", "").replace(" ", "").lower()
                print("The email = " , modified_email)

                
                print("The user is alread exist = ")
                query3 = text(f"DELETE FROM student_information WHERE name = '{data['student_name']}' or form_b = '{data['B_form_number']}';")
                verify = conn.execute(query3)
                print("The row is deleate")
                query4 = text(f"INSERT INTO student_information VALUES ('{modified_email}', '{data['B_form_number']}', '{data['father_name']}', '{data['father_cinc']}', '{data['student_religion']}', '{data['student_gender']}', '{data['student_class']}', '{data['student_dob']}', '{image_path}', '{data['whatsApp_number']}', '{data['last_school_class']}', '{data['student_blood']}', '{data['Elective_subject']}', '{data['student_address']}', '{data['last_school']}', '{data['focacl_person']}', '{data['focacl_person_number']}' , '{count1[0][0]+1}' , '{data['student_name']}' , '{count2[0][0]+1}' , '0')")
                verify = conn.execute(query4)
                print("The row is update")
                if verify:
                    print("username and password is insert in login table")
                    query5 = text(f"INSERT INTO user_login_table VALUES ('{modified_email}', '123', 'student');")
                    conn.execute(query5)
                # flash("you new student data is add successfully")
        return render_template('school_admin_URLs/school_admin_dashboard.html')


    def stored_image_in_file_and_send_path_in_db(self , file , folder_name):
        if file is not None:
            new_filename = str(datetime.now().timestamp()).replace(".", "")  # Generating unique name for the file
            # Spliting ORIGINAL filename to seperate extenstion
            split_filename = file.filename.split(".")
            # Canlculating last index of the list got by splitting the filname
            ext_pos = len(split_filename)-1
            # Using last index to get the file extension
            ext = split_filename[ext_pos]
            img_db_path = str(f"images/{folder_name}/{new_filename}.{ext}")
            print("The type of path  = ", type(img_db_path))
            file.save(f"static/images/{folder_name}/{new_filename}.{ext}")
            print("File uploaded successfully")
            return img_db_path

        
                              
    def search_student_admission_data(self, data):
        print("The is search student admission data")
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM student_information WHERE name = '{data['email_search']}' OR form_b = '{data['b_from_search']}' OR student_registration_number = '{data['student_registration_number']}';")
            user = conn.execute(query).fetchall()
            if user:
                print("the data in user is = ")
                print(user)
                return user
            else:
                return " "
                # return render_template('school_admin_URLs/school_admin_dashboard.html' , data = user)
                
                
    def teacher_joining_information(self , data , image_path):
        with self.engine.connect() as conn:
            print("the data = " , data)
            query1 = text(f"SELECT COUNT(*)  From teacher_information")
            count1 = conn.execute(query1).fetchall()
            
            email = f"{data['teacher_name']}-{count1[0][0]+1}-teacher@iqra.edu"
            modified_email = email.replace("Class ", "").replace(" ", "").lower()
            print("The email = " , modified_email)
            print("The user is alread exist = ")
            query3 = text(f"DELETE FROM teacher_information WHERE name = '{data['teacher_name']}' or cnic_number = '{data['cnic_number']}';")
            verify = conn.execute(query3)
            print("The row is deleate")
            query4 = text(f"INSERT INTO teacher_information VALUES ('{modified_email}', '{data['cnic_number']}', '{data['father_name']}', '{data['father_cinc']}', '{data['teacher_religion']}', '{data['teacher_gender']}', '{data['teaching_class']}', '{data['teacher_dob']}', '{image_path}', '{data['whatsApp_number']}', '{data['teacher_blood']}', '{data['teacher_address']}', '{data['specilized_subject']}', '{data['last_school']}' , '{data['teacher_name']}' , '{count1[0][0]+1}' , '0' );")
            verify = conn.execute(query4)
            print("The row is update")
            if verify:
                    print("username and password is insert in login table")
                    query5 = text(f"INSERT INTO user_login_table VALUES ('{modified_email}', '123', 'teacher');")
                    conn.execute(query5)
                    return True

            flash("you new student data is add successfully")
            return render_template('school_admin_URLs/school_admin_dashboard.html')
            
            
        
        
        
        
    def search_teacher_data(self, data):
        print("The is search  teacher data")
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM teacher_information WHERE name = '{data['email_search']}' OR cnic_number = '{data['cnic_search']}' OR teacher_id = '{data['teacher_ID']}';")
            user = conn.execute(query).fetchall()
            if user:
                print("the data in user is = ")
                print(user)
                return user
            else:
                return " "
                # return render_template('school_admin_URLs/school_admin_dashboard.html' , data = user)

                
        