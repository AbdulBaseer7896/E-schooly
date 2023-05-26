from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request
# from model.teacher_model import teacher_model
import json
from model.teacher_admin_model import teacher_admin_model
import datetime

obj = teacher_admin_model()

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator




@app.route('/teacher_admin/teacher_attandance' ,  methods=["GET", "POST"])
@login_required('teacher_admin' , )
def teacher_attandance():
    print("This is the teacher attandace funciton")
    data = request.args.get('data')
    result = str(data) 
    print("this is restul = " , data)
    result_dict = eval(result)
    if request.method == "GET":
        teacher_name = obj.teacher_name_for_attendance(result_dict)
        print("The is teacher name = " , teacher_name)
        return render_template("teacher_admin_URLs/teacher_attandance.html" , data = result_dict  , info = teacher_name)
    
    if request.method == "POST":
        data = request.form.to_dict()
        print("This is attandance " , data)
        result = []
        for i in range(1, (len(data) // 4) + 2):
            tuple_data = []
            for j in range(1, 5):
                key = f'teacher_email{i}' if j == 1 else f'teacher_cnin{i}' if j == 2 else f'teacher_id{i}' if j == 3 else f'cheek{i}' 
                tuple_data.append(data.get(key))
            result.append(tuple_data)
        print("this is result === " , result)
        obj.mark_teacher_attandance(result)
        print("this is the final result = " , result)
        print(result[1][0])
    return render_template("teacher_admin_URLs/teacher_admin_dashboard.html" , data = result_dict )