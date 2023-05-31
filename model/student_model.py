import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector


class student_model():
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
    
    def take_student_profile_data(self , data):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT * FROM  student_information WHERE name = '{data['email_login']}';")
                result = conn.execute(query1).fetchall()
                print("its also work")
            except:
                query1 = text(f"SELECT * FROM  student_information WHERE name = '{data[0][0]}';")
                result = conn.execute(query1).fetchall()
                print("its work")          
            if result:
                print("This is result of take student " , result)
                return result
            # else:
                # return render_template('login.html')
            
    def take_student_dairy_data(self , data):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT class FROM  student_information WHERE name = '{data['email_login']}';")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT class FROM  student_information WHERE name = '{data[0][0]}';")
                result = conn.execute(query1).fetchall()      
            if result:
                query2 = text(f"SELECT * FROM  teacher_class_period WHERE class_name = '{result[0][0]}';")
                dairy = conn.execute(query2).fetchall() 
                print("This is the dairy of the student = " ,dairy)
                return dairy
            else:
                print("The dairy is not found")
                return render_template('login.html')
            
    def attandance(self , data):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT class FROM  student_information WHERE name = '{data['email_login']}';")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT class FROM  student_information WHERE name = '{data[0][0]}';")
                result = conn.execute(query1).fetchall()      
            if result:
                query2 = text(f"SELECT total_student_attendance FROM  total_attendance WHERE class = '{result[0][0]}';")
                total = conn.execute(query2).fetchall() 
                
                # total_present =  
                if total != []:
                    print("The total = " , total)
                    expression = f"((({total[0][0]} - {data[0][19]})  / {total[0][0]})  * 100)"
                    perstange = round(eval(expression) , 2)
                
                    print("This is the dairy of the student = " , perstange)
                    return perstange
                else:
                    print("The perstange is not found is not found")
                    perstange = 0
                    return perstange
        
        
    def take_student_notification_data(self , data):
        with self.engine.connect() as conn:
            try:
                query1 = text(f"SELECT class FROM  student_information WHERE name = '{data['email_login']}';")
                result = conn.execute(query1).fetchall()
            except:
                query1 = text(f"SELECT class FROM  student_information WHERE name = '{data[0][0]}';")
                result = conn.execute(query1).fetchall()      
            if result:
                print("This is class name =  = " , result[0][0] )
                query2 = text(f"SELECT * FROM  student_notification WHERE class_name = '{result[0][0]}' or class_name = 'school';")
                notification = conn.execute(query2).fetchall() 
                print("This is the dairy of the student = " ,notification)
                return notification
            else:
                print("The notificaton is not found")
                return render_template('login.html')
            
            
    def take_student_result_data(self , data):
        # print("The ioasf dat [ [ ]] = " , data[0][17])
        with self.engine.connect() as conn:
            
            # query1 = text(f"SELECT DISTINCT result_type , result_date , class FROM  result_student_subject_marks WHERE student_email = '{data[0][0]}' or roll_number = '{data[0][17]}';")
            # result = conn.execute(query1).fetchall()  
            # # print("This is the subject of   student = " , result)
            # all_result = []
            # if result:
            #     for item in result:
                    # print("This is ===  = = " , item)
                    # query2 = text(f"SELECT  subject, total_marks, markes , result_type , result_date FROM  result_student_subject_marks WHERE result_type = '{item[0]}' and result_date = '{item[1]}' and class = '{item[2]}' and student_email = '{data[0][0]}' and roll_number = '{data[0][17]}';")
            query2 = text(f"SELECT b_form_name, roll_number , student_email , result_type, subject, markes , total_marks , result_date  FROM result_student_subject_marks WHERE student_email = '{data[0][0]}' ORDER BY result_type;")
            result = conn.execute(query2).fetchall()
                    # print("This is the subject of   student = = = " , result )

            print("Final = = " , result)
                
            return result
            # else: 
            #     print("No result find")
            #     return False
                
                
                
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
        


    