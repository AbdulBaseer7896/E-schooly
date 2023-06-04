from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash
from model.princiap_model import principal_models
import ast
from datetime import datetime, date
from collections import defaultdict

obj = principal_models()

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator



@app.route('/Principal/teacher_periods' , methods=["GET", "POST"])
@login_required('principal')
def teacher_periods():
    name = obj.teacher_names()
    if request.method == 'GET':
        return render_template('principal_URLs/teacher_periods.html' , data = name)
    elif request.method == 'POST':
        dataa = request.form.to_dict()
        print("This is teacher name = " , dataa['teacher_name'])
        print("The data is equal to " , dataa)
        obj.stored_teacher_period_data(dataa)
        obj.make_class_teacher(dataa)
        flash(('Periods are Assigned to Teacher  Successfully !!!' , 'principal_periods'))
        return render_template('principal_URLs/principal_dashboard.html' , data = name)
    
    

# The name and teacher_names function was taken for teacher_periods function. To verifiy it cheek it
@app.route('/Principal/send_principal_notification' , methods=["GET", "POST"])
@login_required('principal')
def send_principal_notification():
    name = obj.teacher_names()
    if request.method == 'GET':
        return render_template('principal_URLs/send_notification.html')
    elif request.method == 'POST':
        info = request.form.to_dict()
        notification_file = request.files['notification_document']
        folder_name = 'Notifications'
        file_path = obj.stored_notification_and_send_path_in_db(notification_file , folder_name)
        if file_path:
            # print("The student name = " , dataa['])
            print("THis is image path as you see = " , file_path)       
            obj.send_principal_notification_of_db(info , file_path)
            flash(('Notification send Successfully !!!' , 'principal_notification'))
            return render_template('principal_URLs/principal_dashboard.html' , data = name)
        


@app.route('/Principal/delete_nofitication_principal', methods=["GET", "POST"])
@login_required('principal')
def delete_nofitication_principal():
    notification_data = obj.take_principal_notification_for_db_for_delete()
    
    if notification_data:
        print("This is notification_data =", notification_data)
        if request.method == 'GET':
            return render_template('principal_URLs/delete_nofitication_principal.html', notification_data=notification_data)
        if request.method == 'POST':
            result = request.form.get('delete_notification')
            result_dict = str(result) 
            delete_notification = eval(result_dict)
            obj.delete_selected_notification_form_data(delete_notification)
            print("Now its endsss")
            flash(("You will Delete the Massage Successfully !!!" , 'delete_notification_principal'))
            return render_template('principal_URLs/principal_dashboard.html')
        
        
@app.route('/Principal/teacher_period_data', methods=["GET", "POST"])
@login_required('principal')
def teacher_period_data():
    teacher_period_data = obj.take_teacher_period_data_for_db()
    
    if teacher_period_data:
        print("This is notification_data =", teacher_period_data)
        
        grouped_data = defaultdict(list)
        for class_data in teacher_period_data:
            class_name = class_data[0]
            grouped_data[class_name].append(class_data)

        teacher_period_data_grouped = list(grouped_data.values())
    if request.method == 'GET':
            return render_template('principal_URLs/teacher_period_data.html' , teacher_period_data_grouped = teacher_period_data_grouped)
