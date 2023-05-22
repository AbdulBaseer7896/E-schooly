import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector


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

    def student_admission_data(self, data):
        with self.engine.connect() as conn:
                B_form_number = data['B_form_number']
                query1 = text(f"SELECT * FROM  student_information WHERE form_b = '{data['B_form_number']}';")
                cheek = conn.execute(query1).fetchall()
                if cheek:
                    print("The user is alread exist = ")
                    query2 = text(f"UPDATE student_information SET name = '{data['student_name']}', form_b = '{data['B_form_number']}' ,  father_name = '{data['father_name']}', father_cnic = '{data['father_cinc']}', religion = '{data['student_religion']}', gender = '{data['student_gender']}', class = '{data['student_class']}', dob = '{data['student_dob']}', pic = '{data['student_image']}', whatapp_number = '{data['whatsApp_number']}', last_class = '{data['last_school_class']}', Blood = '{data['student_blood']}', elective_subject = '{data['Elective_subject']}', address = '{data['student_address']}', last_school = '{data['last_school']}', focacl_name = '{data['focacl_person']}', focacl_number = '{data['focacl_person_number']}' WHERE form_b = {B_form_number};")
                    user = conn.execute(query2)
                else:
                    query3 = text(f"INSERT INTO student_information VALUES ('{data['student_name']}', '{data['B_form_number']}', '{data['father_name']}', '{data['father_cinc']}', '{data['student_religion']}', '{data['student_gender']}', '{data['student_class']}', '{data['student_dob']}', '{data['student_image']}', '{data['whatsApp_number']}', '{data['last_school_class']}', '{data['student_blood']}', '{data['Elective_subject']}', '{data['student_address']}', '{data['last_school']}', '{data['focacl_person']}', '{data['focacl_person_number']}');")
                    user = conn.execute(query3)
                # flash("you new student data is add successfully")
        return render_template('school_admin_URLs/school_admin_dashboard.html')


        
                              
    def search_student_admission_data(self, data):
        print("The is search student admission data")
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM student_information WHERE name = '{data['email_search']}' OR form_b = '{data['b_from_search']}' OR father_cnic = '{data['father_cnic_search']}';")
            user = conn.execute(query).fetchall()
            if user:
                print("the data in user is = ")
                print(user)
                return user
            else:
                return " "
                # return render_template('school_admin_URLs/school_admin_dashboard.html' , data = user)
                
                
    def teacher_joining_information(self , data):
        with self.engine.connect() as conn:
            cnin_number = data['cnin_number']
            query1 = text(f"SELECT * FROM  teacher_information WHERE cnic_number = '{data['cnin_number']}';")
            cheek = conn.execute(query1).fetchall()
            if cheek:
                print("The user is alread exist = ")
                query2 = text(f"UPDATE teacher_information SET name = '{data['teacher_name']}', cnic_number = '{data['cnic_number']}' ,  father_name = '{data['father_name']}', father_cnic = '{data['father_cinc']}', religion = '{data['teacher_religion']}', gender = '{data['teacher_gender']}', class = '{data['teaching_class']}', dob = '{data['teacher_dob']}', pic = '{data['teacher_image']}', whatapp_number = '{data['whatsApp_number']}',  Blood = '{data['teacher_blood']}' , address = '{data['teacher_address']}' ,  '{data['last_school']}' WHERE cnic_number  = {'cnin_number'};")
                user = conn.execute(query2)
            else:
                # query3 = text(f"INSERT INTO teacher_information VALUES ('{data['teacher_name']}', '{data['cnin_number']}', '{data['father_name']}', '{data['father_cinc']}', '{data['teacher_religion']}', '{data['teacher_gender']}', '{data['teaching_class']}', '{data['teacher_dob']}', '{data['teacher_image']}', '{data['whatsApp_number']}', '{data['teacher_blood']}, '{data['teacher_address']}', '{data['specilized_subject']}' , '{data['last_school']}' );")
                query3 = text(f"INSERT INTO teacher_information VALUES ('{data['teacher_name']}', '{data['cnin_number']}', '{data['father_name']}', '{data['father_cinc']}', '{data['teacher_religion']}', '{data['teacher_gender']}', '{data['teaching_class']}', '{data['teacher_dob']}', '{data['teacher_image']}', '{data['whatsApp_number']}', '{data['teacher_blood']}', '{data['teacher_address']}', '{data['specilized_subject']}', '{data['last_school']}');")

                user = conn.execute(query3)
            # flash("you new student data is add successfully")
        return render_template('school_admin_URLs/school_admin_dashboard.html')
            
            
        
        
        
        
    def search_teacher_data(self, data):
        print("The is search  teacher data")
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM teacher_information WHERE name = '{data['email_search']}' OR cnic_number = '{data['cnic_search']}' OR father_cnic = '{data['father_cnic_search']}';")
            user = conn.execute(query).fetchall()
            if user:
                print("the data in user is = ")
                print(user)
                return user
            else:
                return " "
                # return render_template('school_admin_URLs/school_admin_dashboard.html' , data = user)

                
        