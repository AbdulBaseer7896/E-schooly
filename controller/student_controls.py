from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash
from model.student_model import student_model
from model.school_admin_model import school_admin_models
import datetime


obj = student_model()

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator



@app.route('/student/profile' ,  methods=["GET", "POST"] )
@login_required('student')
def student_profile():
    # Functionality for teacher dashboard
    print("This is student profile")
    data = request.args.get('data')
    result = str(data) 
    print("This is data of student profile " , data)
    # Parse the string representation of the dictionary back to a dictionary object
    result_dict = eval(result)
    result = obj.take_student_profile_data(result_dict)
    print("this is result " , result)
    attandance = obj.attandance(result)
    return render_template('student_URLs/student_profile.html' , data = result  , attandance = attandance )



@app.route('/student/dairy' , methods=["GET", "POST"] )
@login_required('student')
def student_dairy():
    print("This is student dairy")
    data = request.args.get('data')
    print("This is data of student_dairy " , data)
    result = str(data) 
    
    result_dict = eval(result)
    print("This is result dict ", result_dict)
    dairy = obj.take_student_dairy_data(result_dict)
    dairy.reverse()
    print("This is result as you see = " , dairy)
    return render_template('student_URLs/student_dairy.html' , dairy = dairy , data = data)




@app.route('/student/student_notification' , methods=["GET", "POST"] )
@login_required('student')
def student_notification():
    print("This is student dairy")
    data = request.args.get('data')
    print("This is data of student_dairy " , data)
    result = str(data) 
    
    result_dict = eval(result)
    print("This is result dict ", result_dict)
    notification = obj.take_student_notification_data(result_dict)
    notification.reverse() 
    print("This is result as you see = " , notification)
    if request.method == "GET":
        return render_template('student_URLs/student_notification.html' , notification = notification , data = data)
    
    
    

@app.route('/student/student_result' , methods=["GET", "POST"] )
@login_required('student')
def student_result():
    print("This is student dairy")
    data = request.args.get('data')
    print("This is data of student_dairy " , data)
    result = str(data) 
    
    result_dict = eval(result)
    print("This is result dict ", result_dict)
    result_data = obj.take_student_result_data(result_dict)
    if result_data:
        print("This is 99999999999999999999999999")

        grouped_data = {}  # Dictionary to group data by exam type and date

        for item in result_data:
            exam_type = item[3]
            exam_date = item[7]

            key = (exam_type, exam_date)

            if key not in grouped_data:
                grouped_data[key] = []

            grouped_data[key].append(item)

        # Access and print specific rows
    number_of_results =  len(list(grouped_data.keys()))
    specific_rows = list(grouped_data.keys())
    len(specific_rows)
    print("hello")
    for i in range(0 , number_of_results):
        specific_row = grouped_data[specific_rows[i]]


    # # Access a specific element from the row
        for j in range(0 , len(specific_row)):
            specific_element = specific_row[j][4]
            print(specific_row[j][3])
            print(specific_element)
    
    print("its work")

    if request.method == "GET":
        updated_grouped_data = {}  # Dictionary to store updated data

        for key, rows in grouped_data.items():
            total_marks = 0
            obtain_marks = 0
            for row in rows:
                total_marks += row[6]
                obtain_marks += row[5]

            updated_key = (*key, total_marks, obtain_marks)  # Create a new tuple with updated values
            updated_grouped_data[updated_key] = rows  # Add the updated key to the dictionary

        return render_template('student_URLs/student_result.html', result_data=result_data, data=data, specific_rows=specific_rows, grouped_data=updated_grouped_data)
    
    
