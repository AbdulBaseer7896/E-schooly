from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash
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
@login_required('teacher_admin')
def teacher_attandance():
    print("This is the teacher attandace funciton")
    data = request.args.get('data')
    result = str(data) 
    print("this is restul = " , data)
    result_dict = eval(result)
    teacher_name = obj.teacher_name_for_attendance(result_dict)
    print("The is teacher name = " , teacher_name)
    if not teacher_name:
            flash(("There is not teacher in the data base Contact with Admin!!!" , 'no_teacher_for_attandance'))
            return render_template("teacher_admin_URLs/teacher_admin_dashboard.html" , data = result_dict )
    else:    
        if request.method == "GET":
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
        teacher_information = request.form.get("teacher_information")
        print(result[1][0])
        flash(('Teacher Attendance Upload Successfully !!!' , 'teacher_attandance'))
        return render_template("teacher_admin_URLs/teacher_admin_dashboard.html" , data = teacher_information )



@app.route('/teacher_admin/teacher_notification' ,  methods=["GET", "POST"])
@login_required('teacher_admin')
def teacher_notification():
    data = request.args.get('data')
    result = str(data) 
    print("this is restul = " , data)
    result_dict = eval(result)
    if request.method == "GET":
        return render_template('teacher_admin_URLs/teacher_notification.html' , data = data)
    elif request.method == "POST":
        notification = request.form.to_dict()
        notification_file = request.files['notification_document']
        if  notification_file.filename != '':
            folder_name = 'Notifications'
            file_path = obj.stored_notification_in_file_and_send_path_in_db(notification_file , folder_name)
        else:
            file_path = ''

        print("THis is image path as you see = " , file_path)
        obj.send_notification_of_db(notification , file_path)
        flash(('The Notification is Send to ALl Teacher Successfully !!! ' , 'teacher_notification'))
        return render_template('teacher_admin_URLs/teacher_admin_dashboard.html' , data = data)
        
        
        

@app.route('/teacher_admin/delete_notification_admin_teacher', methods=["GET", "POST"])
@login_required('teacher_admin')
def delete_notification_admin_teacher():
    data = request.args.get('data')
    result = str(data) 
    print("this is restul = " , data)
    result_dict = eval(result)
    notification_data = obj.take_techer_admin_notification_for_db_for_delete()
    if notification_data:
        print("This is notification_data =", notification_data)
        if request.method == 'GET':
            return render_template('teacher_admin_URLs/delete_notification_admin_teacher.html', notification_data=notification_data , data = data)
    if request.method == 'POST':
        result = request.form.get('delete_notification')
        result_dict = str(result) 
        delete_notification = eval(result_dict)
        obj.delete_selected_notification_form_data(delete_notification)
        print("Now its endsss")
        flash(("You will Delete the Massage Successfully !!!" , 'delete_notification_teacher_admin'))
        return render_template('teacher_admin_URLs/teacher_admin_dashboard.html' , data = data)
    else:
        flash(("You could not send any Massage to teacher !!! kindly send the massage !!!" , 'no_massage_to_delete_teacher_admin'))
        return render_template('teacher_admin_URLs/teacher_admin_dashboard.html' , data = data)