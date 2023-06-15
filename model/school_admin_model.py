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

    def student_admission_data(self, data , image_path , student_id):
        print("This is data ", student_id)
        with self.engine.connect() as conn:
                query_delete_email = text(f"DELETE FROM user_login_table WHERE user_name = '{student_id}' And user_type = 'student';")
                conn.execute(query_delete_email)
                
                print("Teh aij fsidj ai dfk  as k " , data['student_name'])
                print(data)
                query1 = text(f"DELETE FROM student_information WHERE name = '{data['student_email']}';")
                conn.execute(query1)
                print("The row is deleate")
                
                query2 = text(f"SELECT  MAX(CAST(student_roll_number AS UNSIGNED))From student_information WHERE class = '{data['student_class']}';")
                roll_number_max = conn.execute(query2).fetchall()
                query3 = text(f"SELECT COALESCE(MIN(t1.student_roll_number) + 1, MAX(t1.student_roll_number) + 1, 1) AS missing_or_max_number FROM (SELECT DISTINCT student_roll_number   FROM student_information   WHERE class = '{data['student_class']}' ) AS t1 LEFT JOIN (   SELECT DISTINCT student_roll_number   FROM student_information   WHERE class = '{data['student_class']}' ) AS t2 ON t1.student_roll_number + 1 = t2.student_roll_number WHERE t2.student_roll_number IS NULL;")
                roll_number_missing = conn.execute(query3).fetchall()

                query4 = text(f"SELECT MAX(CAST(student_registration_number AS UNSIGNED)) FROM student_information;")
                registration_number_max = conn.execute(query4).fetchall()
                query5 = text(f"SELECT COALESCE(MIN(t1.student_registration_number + 1), MAX(t1.student_registration_number) + 1, 1) AS missing_or_max_number FROM (SELECT DISTINCT CAST(student_registration_number AS UNSIGNED) AS student_registration_number   FROM student_information ) AS t1 LEFT JOIN ( SELECT DISTINCT CAST(student_registration_number AS UNSIGNED) AS student_registration_number   FROM student_information ) AS t2 ON t1.student_registration_number + 1 = t2.student_registration_number WHERE t2.student_registration_number IS NULL;")
                registration_number_missing = conn.execute(query5).fetchall()
                
                if roll_number_max == roll_number_missing:
                    roll_number_final = roll_number_max[0][0]
                else:
                    roll_number_final = roll_number_missing[0][0] -1

                if registration_number_max == registration_number_missing:
                    registration_number_final = registration_number_max[0][0]
                else:
                    registration_number_final = registration_number_missing[0][0] -1
                
                email = f"{data['student_name']}-{int(roll_number_final) +1}-{int(registration_number_final) + 1}-{data['student_class']}@iqra.edu"
                modified_email = email.replace("Class ", "").replace(" ", "").lower()
                print("The email = " , modified_email)
                

                query4 = text(f"INSERT INTO student_information VALUES ('{modified_email}', '{data['B_form_number']}', '{data['father_name']}', '{data['father_cinc']}', '{data['student_religion']}', '{data['student_gender']}', '{data['student_class']}', '{data['student_dob']}', '{image_path}', '{data['whatsApp_number']}', '{data['last_school_class']}', '{data['student_blood']}', '{data['Elective_subject']}', '{data['student_address']}', '{data['last_school']}', '{data['focacl_person']}', '{data['focacl_person_number']}' , '{int(roll_number_final +1)}' , '{data['student_name']}' , '{registration_number_final +1}' , '0')")
                verify = conn.execute(query4)

                print("The row is update")
                if verify:
                    print("username and password is insert in login table")
                    query5 = text(f"INSERT INTO user_login_table VALUES ('{modified_email}', '123', 'student');")
                    conn.execute(query5)
                
                flash(("New student data is add successfully!!!" , 'new_student_data'))
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
                
                
    def teacher_joining_information(self , data , image_path , teacher_id):
        with self.engine.connect() as conn:
            query_delete_email = text(f"DELETE FROM user_login_table WHERE user_name = '{teacher_id}' And user_type = 'teacher';")
            conn.execute(query_delete_email)
            
            print("the data = " , teacher_id)
            print("This is data sk asdi ja = = = " , data)
            query2 = text(f"DELETE FROM teacher_information WHERE name = '{teacher_id}';")
            verify = conn.execute(query2)
            print("The row is deleate")
            
            
            query1 = text(f"SELECT  MAX(CAST(teacher_id AS UNSIGNED)) From teacher_information")
            teacher_new_id_max = conn.execute(query1).fetchall()
            query1 = text(f"SELECT COALESCE(MIN(t1.teacher_id + 1), MAX(t1.teacher_id) + 1, 1) AS missing_or_max_number FROM (   SELECT DISTINCT CAST(teacher_id AS UNSIGNED) AS teacher_id   FROM teacher_information ) AS t1 LEFT JOIN (   SELECT DISTINCT CAST(teacher_id AS UNSIGNED) AS teacher_id   FROM teacher_information ) AS t2 ON t1.teacher_id + 1 = t2.teacher_id WHERE t2.teacher_id IS NULL;")
            teacher_new_id_missing = conn.execute(query1).fetchall()
            
            if teacher_new_id_max == teacher_new_id_missing:
                teacher_id_final = teacher_new_id_max[0][0]
            else:
                teacher_id_final = teacher_new_id_missing[0][0] -1
                
            print("This is ighuoas h finsodhg o 989879  = " , teacher_id_final)
            email = f"{data['teacher_name']}-{teacher_id_final +1}-teacher@iqra.edu"
            modified_email = email.replace("Class ", "").replace(" ", "").lower()
            print("The email = " , modified_email)
            print("The user is alread exist = ")
            query3 = text(f"INSERT INTO teacher_information VALUES ('{modified_email}', '{data['cnic_number']}', '{data['father_name']}', '{data['father_cinc']}', '{data['teacher_religion']}', '{data['teacher_gender']}', '{data['teaching_class']}', '{data['teacher_dob']}', '{image_path}', '{data['whatsApp_number']}', '{data['teacher_blood']}', '{data['teacher_address']}', '{data['specilized_subject']}', '{data['last_school']}' , '{data['teacher_name']}' , '{teacher_id_final + 1}' , '0' );")
            conn.execute(query3)
            print("The row is update . . . " , modified_email)

            print("username and password is insert in login table")
            query4 = text(f"INSERT INTO user_login_table VALUES ('{modified_email}', '123', 'teacher');")
            conn.execute(query4)
            return True

            
        
        
        
        
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




    def take_student_result_data(self , data):
        print("This is sj foiajsgoi jsogj aosjgo ja   = = = = " , data)
        with self.engine.connect() as conn:
            query1 = text(f"SELECT b_form_name, roll_number , student_email , result_type, subject, markes , total_marks , result_date  FROM result_student_subject_marks WHERE student_email = '{data}' ORDER BY result_type, result_date DESC;")
            result = conn.execute(query1).fetchall()
            return result

                
                
    def calculate_student_result(self , data):
        print("This is calculated data ==== " , data)
        marks_sum = {}
        for item in data:
            exam_type = item[3]
            exam_date = item[7]
            marks = item[5]

            # Create a unique key by combining exam type and date
            key = (exam_type, exam_date)

            # Check if the key already exists in the dictionary
            if key in marks_sum:
                marks_sum[key] += marks
            else:
                marks_sum[key] = marks
                
        # Print the sum of marks for each exam type and date
        for key, sum_marks in marks_sum.items():
            print(f"Exam Type: {key[0]}, Date: {key[1]} - Total Marks: {sum_marks}")
            
        return marks_sum
        
        
        
    def search_user_data_for_forger_password(self , data):
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
                
            elif data['login-val'] == 'principal':
                print("This is principal")
                query = text(f"SELECT * FROM user_login_table WHERE user_name = '{data['email_search']}' OR user_type = 'principal';")
                user = conn.execute(query).fetchall()
            
            if user:
                print("the data in user is = ")
                print(user)
                return user
            else:
                return False
        
    def search_user_passwrod(self , data):
        print("The data = d = = 99999 = " , data)
        print("The data = d = = 99999 = " , data[0][0])
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM user_login_table WHERE user_name = '{data[0][0]}';")
            user = conn.execute(query).fetchall()
            return user
        


        
    def take_student_attandance_for_db(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT b_form_name ,class , whatapp_number , student_registration_number , student_attendance  FROM student_information ORDER BY student_attendance DESC;")
            user = conn.execute(query).fetchall()
            return user
        
    
    def take_total_number_of_working_days_of_student(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT total_student_attendance  , class FROM total_attendance;")
            user = conn.execute(query).fetchall()
            return user
        