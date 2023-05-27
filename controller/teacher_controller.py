from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request
from model.teacher_model import teacher_model
import json
# from model.school_admin_model import school_admin_models
import datetime

obj = teacher_model()

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator



@app.route('/teacher/profile')
@login_required('teacher')
def teacher_profile():
    # Functionality for teacher dashboard
    data = request.args.get('data')
    result = str(data) 
    print("this is restul" , data)
    result_dict = eval(result)
    # Parse the string representation of the dictionary back to a dictionary object
    if request.method == "GET":
        profile_data = obj.take_teacher_profile_data(result_dict)
        attandance = obj.teacher_attandance(profile_data)
        return render_template('teacher_URLs/teacher_profile.html' , profile_data = profile_data , data = data , attandance = attandance)
    if request.method == "POST":
        return render_template('teacher_URLs/teacher_dashboard.html' , data = data)
        




@app.route('/teacher/upload_dairy' , methods=["GET", "POST"] )
@login_required('teacher')
def upload_dairy():
    data = request.args.get('data')
    if request.method == "GET":
        result = str(data) 
        result_dict = eval(result)
        result = obj.take_teacher_class_and_period_data(result_dict)
        return render_template("teacher_URLs/upload_dairy.html" , data = result)
    elif request.method == 'POST':
        data = request.form.to_dict()
        print("This is data of upload dairy = " , data)
        result = obj.cross_cheed_class_period(data)
        if result:
            print(data)
            return render_template("teacher_URLs/upload_dairy_form.html" , data = data)
        else:
            return render_template('teacher_URLs/teacher_dashboard.html')
        



@app.route('/teacher/write_dairy' , methods=["GET", "POST"] )
@login_required('teacher')
def upload_dairy_form():
    if request.method == "GET":
        return render_template('teacher_URLs/upload_dairy_form.html')
    elif  request.method == 'POST':
        data = request.form.to_dict()
        print("This is dairy " , data)
        obj.send_dairy(data)
        return render_template("teacher_URLs/teacher_dashboard.html")
        # else:
        #     return render_template('teacher_URLs/teacher_dashboard.html')
        
        
@app.route('/teacher/student_attendance' , methods=["GET", "POST"] )
@login_required('teacher')
def student_attendance():
    data = request.args.get('data')
    result = str(data) 
    result_dict = eval(result)
    print("The data is == " , result_dict)
    # print("The teacher name  = " , result_dict['email_login'])
    if request.method == "GET":
        student_name = obj.class_student_name_for_attendance(result_dict)
        return render_template("teacher_URLs/student_attendance.html" , data = data  , info = student_name)
    
    if request.method == "POST":
        attandance = request.form.to_dict()
        print("This is attandance " , attandance)
        result = []
        for i in range(1, (len(attandance) // 3) + 1):
            tuple_attandance = []
            for j in range(1, 5):
                key = f'student_email{i}' if j == 1 else f'student_class{i}' if j == 2 else f'student_roll_number{i}' if j == 3 else f'cheek{i}' 
                tuple_attandance.append(attandance.get(key))
            result.append(tuple_attandance)
        obj.mark_student_attandance(result)
        print("this is the final result = " , result)
        print(result[1][0])
        print("This is data - " , data)
        return render_template("teacher_URLs/teacher_dashboard.html" , data = data)
    
    
    
@app.route('/teacher/notification_for_teacher' , methods=["GET", "POST"] )
@login_required('teacher')
def notification_for_teacher():
    data = request.args.get('data')
    if request.method == "GET":
        notification = obj.take_notification_details()
        print(notification)
        return render_template("teacher_URLs/notification.html" , notification = notification , data = data )
    
    return render_template('teacher_URLs/notification.html' ,  data = data)





@app.route('/teacher/send_notification_to_student' , methods=["GET", "POST"] )
@login_required('teacher')
def send_notification_to_student():
    data = request.args.get('data')
    result = str(data) 
    result_dict = eval(result)
    print("The data is == " , result_dict)
    # print("This is teacher class = " , teacher_class[0][0])
    if request.method == "GET":
        teacher_class = obj.take_teacher_class_form_db(result_dict)
        print("The teacher class os = " , teacher_class)
        return render_template("teacher_URLs/send_notification_to_student.html" , data = result_dict , teacher_class = teacher_class)
    elif request.method == "POST":
        data = request.form.to_dict()
        print("The data is = " , data)
        obj.send_student_notification_to_db(data)
        return render_template('teacher_URLs/teacher_dashboard.html' ,data = result_dict)
    # return render_template('teacher_URLs/send_notification_to_student.html')