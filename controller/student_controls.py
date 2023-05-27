from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request
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
    print("This is result as you see = " , notification)
    return render_template('student_URLs/student_notification.html' , data = notification)
