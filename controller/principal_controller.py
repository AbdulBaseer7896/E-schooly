from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash
from model.princiap_model import principal_models

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
        

