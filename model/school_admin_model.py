import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector


class user_model():
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
                query = text(f"INSERT INTO student_information VALUES ('{data['student_name']}', '{data['B_form_number']}', '{data['father_name']}', '{data['father_cinc']}', '{data['student_religion']}', '{data['student_gender']}', '{data['student_class']}', '{data['student_dob']}', '{data['student_image']}', '{data['whatsApp_number']}', '{data['last_school_class']}', '{data['student_blood']}', '{data['Elective_subject']}', '{data['student_address']}', '{data['last_school']}', '{data['focacl_person']}', '{data['focacl_person_number']}');")
                user = conn.execute(query)
                # flash("you new student data is add successfully")
                return render_template('school_admin_URLs/school_admin_dashboard.html')

                
        