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
    
    print("This is notification_data =", notification_data)
    if notification_data:
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
    else:
        flash(("You will not send any notification !!! Kinldy send it !!!" , "no_notifitaion_to_deleate_for_principal"))
        return render_template('principal_URLs/principal_dashboard.html')
        
        
@app.route('/Principal/teacher_period_data', methods=["GET", "POST"])
@login_required('principal')
def teacher_period_data():
    teacher_period_data = obj.take_teacher_period_data_for_db()
    
    if teacher_period_data:
        print("This is period _data =", teacher_period_data)
        
        grouped_data = defaultdict(list)
        for class_data in teacher_period_data:
            class_name = class_data[0]
            grouped_data[class_name].append(class_data)

        teacher_period_data_grouped = list(grouped_data.values())
        if request.method == 'GET':
            return render_template('principal_URLs/teacher_period_data.html' , teacher_period_data_grouped = teacher_period_data_grouped)
    flash(("You will not assigned any Period to any teacher !!!" , 'no_period_assigned_by_principal'))
    return render_template('principal_URLs/principal_dashboard.html')




        
@app.route('/Principal/class_teacher_data', methods=["GET", "POST"])
@login_required('principal')
def class_teacher_data():
    class_teachers = obj.take_class_teacher_data_for_db()
    # print("This is class teacher oaw jfij  " , class_teachers[0][0])
    if not class_teachers:
        flash(("You will not make any class teacher, Kinldy make the class teacer early !!!" , 'no_class_teacher'))
        return render_template('principal_URLs/principal_dashboard.html')
    
    if request.method == 'GET':
            return render_template('principal_URLs/class_teacher_data.html' , class_teachers = class_teachers )






@app.route('/principal/seach_student_result' , methods=["GET", "POST"])
@app.route('/principal/display_student_result' , methods=["GET", "POST"])
@login_required('principal')
def seach_student_result_principal():
    if request.method == "GET":
        return render_template('principal_URLs/search_result_for_principal.html')
    if request.method =="POST":
        data = request.form.to_dict()
        print("This ijsa fi = " , data)
        result = obj.search_student_admission_data_for_principal(data)
        print("This is isfoands g g )))))))))) = " , result)
        student_name =  result[0][0]
    
        marks_result = obj.take_student_result_data_for_principal(student_name)
        print("this is resoijsf iaisgj  = =  + , ", marks_result)
        
        grouped_data = {}  # Dictionary to group data by exam type and date

        for item in marks_result:
            exam_type = item[3]
            exam_date = item[7]

            key = (exam_type, exam_date)

            if key not in grouped_data:
                grouped_data[key] = []

            grouped_data[key].append(item)

        updated_grouped_data = {}  # Dictionary to store updated data

        for key, rows in grouped_data.items():
            total_marks = 0
            obtain_marks = 0
            for row in rows:
                total_marks += row[6]
                obtain_marks += row[5]

            updated_key = (*key, total_marks, obtain_marks)  # Create a new tuple with updated values
            updated_grouped_data[updated_key] = rows  # Add the updated key to the dictionary

        combined_data = {}

        for key, value in grouped_data.items():
            exam_type, exam_date = key
            score = updated_grouped_data.get(key)

            combined_data[key] = {
                'Total': score,
                'students': value
            }

        return render_template('principal_URLs/dispaly_student_result_to_principal.html', result_data=marks_result, data=data, grouped_data=updated_grouped_data, combined_data=combined_data)

    
    
    
    
@app.route('/principal/forget_password_by_principal' , methods=["GET", "POST"])
@login_required('principal')
def forget_password_by_principal():
    if request.method == "GET":
        flash(("Do Not Share User Personal Information to Any Body !!! Except User Parents !!!" , 'forget_password_warrning_principal'))
        return render_template('principal_URLs/forget_password_by_principal.html')
    elif request.method == 'POST':
        data = request.form.to_dict()
        print("This is data = = " , data)
        result = obj.search_user_data_for_forger_password_by_principal(data)
        print("The result is si si =  = " , result)
        if result:
                password_data = obj.search_user_passwrod_by_principal(result)
                print("This is password data is = == = " , password_data)
                return render_template('principal_URLs/display_password_principal.html' , data = data , password_data = password_data , result = result)
        else:
            flash(("That user could not exit !!! Recheck the User-type And Search Information !!!" , 'no_user_found_for_forget_password_principal'))
            return render_template("principal_URLs/forget_password_by_principal.html" , data = data)
        
        
@app.route('/principal/check_teacher_attandance', methods=["GET", "POST"])
@login_required('principal')
def check_teacher_attandance():
    if request.method == "GET":
        attendance = obj.take_teacher_attandance_for_db()
        total_attendance = obj.take_total_number_of_working_days_of_teacher()
        
        return render_template('principal_URLs/teacher_attandance.html', attendance=attendance, total_attendance=total_attendance)



@app.route('/principal/upload_image_by_principal', methods=["GET", "POST"])
@login_required('principal')
def upload_image_by_principal():
    if request.method == "GET":
        return render_template('principal_URLs/upload_photos.html')
    elif request.method == 'POST':
        data = request.form.to_dict()
        image_file = request.files['image_file']
        folder_name = data['target_area']
        print("This is folder name = = " , folder_name)
        if image_file and image_file.filename:
            print("Thisj ijfid if image _ file = = " , image_file)
            image_path = obj.stored_school_images_and_send_path_in_db(image_file , folder_name)
        else:
            print("There is not image at alll ija ")
            image_path = ""

        if image_path:
            # print("The student name = " , dataa['])
            print("THis is image path as you see = " , image_path) 
            print("This is data = = " , data)
            obj.stored_school_image_path_to_db(data , image_path)
            flash(("New Image Upload Successfully!!! " , "image_upload_done"))
            return render_template('principal_URLs/principal_dashboard.html')
    
        
    

