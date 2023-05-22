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
    result = obj.take_teacher_profile_data(result_dict)
    return render_template('teacher_URLs/teacher_profile.html' , data = result )




@app.route('/teacher/upload_dairy' , methods=["GET", "POST"] )
@login_required('teacher')
def upload_dairy():
    if request.method == "GET":
        data = request.args.get('data')
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