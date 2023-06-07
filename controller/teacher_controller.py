from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash
from model.teacher_model import teacher_model
import json
from flask import flash
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
    print("this is restul" , data)
    result = str(data) 
    result_dict = eval(result)
    print("The  isdjf ioisd fi jsj i === = = " , result_dict)
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
            print("this is 00 " , data)
            return render_template("teacher_URLs/upload_dairy_form.html" , data = data)
        else:
            return render_template('teacher_URLs/teacher_dashboard.html', data = data)
        



@app.route('/teacher/write_dairy' , methods=["GET", "POST"] )
@login_required('teacher')
def upload_dairy_form():
    data = request.args.get('data')
    if request.method == "GET":
        return render_template('teacher_URLs/upload_dairy_form.html')
    elif  request.method == 'POST':
        data = request.form.to_dict()
        image_file = request.files['helping_notes_file']
        folder_name = 'student_dairy_files'
        image_path = obj.stored_dariy_in_file_and_send_path_in_db(image_file , folder_name)
        if image_path:
            # print("The student name = " , dataa['])
            print("THis is image path as you see = " , image_path)
            obj.send_dairy(data , image_path )

            flash(('Class Attandance will Upload Successfully !!!' , 'student_dairy_done'))
    return render_template("teacher_URLs/teacher_dashboard.html", data = data)
        # else:
        #     return render_template('teacher_URLs/teacher_dashboard.html')
        
        
@app.route('/teacher/student_attendance' , methods=["GET", "POST"] )
@login_required('teacher')
def student_attendance():
    data = request.args.get('data')
    result = str(data) 
    result_dict = eval(result)
    print("The teacher name  = " , result_dict)
    # print("The data is == " , result_dict['email_login'])
    if request.method == "GET":
        student_name = obj.class_student_name_for_attendance(result_dict)
        if student_name != False:
            flash(('Just Tick those Students Who are Absend in Class !!!' , 'student_attendance_warning'))
            return render_template("teacher_URLs/student_attendance.html" , data = result_dict  , info = student_name)
        else:
            print("There is not student in you class")
            # flash(("There is not student in you class" , 'warning'))
            return render_template("teacher_URLs/teacher_dashboard.html" , data = data )
    
    if request.method == "POST":
        attandance = request.form.to_dict()
        print("This is attandance " , attandance)
        teacher_mail =  request.form.get('email_login')
        print("This ij difoj asoijf8 udf08u w  = = " , teacher_mail)
        
        
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
        print("This is data - " , teacher_mail)
        flash(('The Attandance is Upload Successfully !!!' , 'sudent_attandance_done'))
    return render_template("teacher_URLs/teacher_dashboard.html" , data = teacher_mail)
    
    
    
@app.route('/teacher/notification_for_teacher' , methods=["GET", "POST"] )
@login_required('teacher')
def notification_for_teacher():
    data = request.args.get('data')
    if request.method == "GET":
        notification = obj.take_notification_details()
        print("THiodsa iofjasd iojf  = ", notification)
        if notification:
            notification.reverse()
            print(notification)
            return render_template("teacher_URLs/notification.html" , notification = notification , data = data )
    flash(("NO notification Will be recived at you ID !!!" , 'no_notification_for_teacher'))
    return render_template('teacher_URLs/teacher_dashboard.html' ,  data = data)





@app.route('/teacher/send_notification_to_student' , methods=["GET", "POST"] )
@login_required('teacher')
def send_notification_to_student():
    data = request.args.get('data')
    result = str(data) 
    result_dict = eval(result)
    print("The data is == " , result_dict)

    if request.method == "GET":
        teacher_class = obj.take_teacher_class_form_db(result_dict)
        print("The teacher class os = " , teacher_class)
        if teacher_class[0][0] == 'Helper':
            flash(("Sorry You are not a class teacer thats why you will not sent the notification to students " , 'not_a_class_teacher_of_send_notification'))
            return render_template('teacher_URLs/teacher_dashboard.html' ,  data = data)
        else:
            return render_template("teacher_URLs/send_notification_to_student.html" , data = result_dict , teacher_class = teacher_class)

    elif request.method == "POST":
        data = request.form.to_dict()
        notification_file = request.files['notification_document']
        if  notification_file.filename != '':
            folder_name = 'Notifications'
            file_path = obj.stored_dariy_in_file_and_send_path_in_db(notification_file , folder_name)
        else:
            file_path = ''
            # print("The student name = " , dataa['])
            print("THis is image path as you see = " , file_path)
            obj.send_student_notification_to_db(data , file_path)
        flash(('The Notification is send to All Student successfully !!!' ,'class_student_notification_done'))
        return render_template('teacher_URLs/teacher_dashboard.html' ,data = data)
    # return render_template('teacher_URLs/send_notification_to_student.html')
    
    
    
@app.route('/teacher/upload_result' , methods=["GET", "POST"] )
@login_required('teacher')
def upload_result():
    data = request.args.get('data')
    result = str(data) 
    result_dict = eval(result)
    print("The data is == " , result_dict)
    if request.method == "GET":
        teacher_class = obj.take_teacher_class_form_db(result_dict)
        student_info = obj.take_class_student_id_form_db(teacher_class)
        class_subject = obj.take_class_subject_from_db(teacher_class)
        if student_info == None or class_subject == None or teacher_class == None:
            flash(("In you class not student exist OR you are not a class teacher of any class" , 'no_student_for_upload_result'))
            return render_template('teacher_URLs/teacher_dashboard.html' , data = data )
        else:
            return render_template('teacher_URLs/upload_result.html' , data = data ,class_subject= class_subject ,  teacher_class = teacher_class , student_info = student_info)
    elif request.method == "POST":
        student_restult = request.form.to_dict()
        result_type_data = (student_restult['restul_type'] , student_restult['date'], student_restult['subject_total_marks'])
        print("The type of result is = " , result_type_data)
        print("The data is = " , student_restult)
        student_marks = []
        for i in range(1, (len(student_restult) // 5) + 1):
            tuple_attandance = []
            for j in range(1, 7):
                key = f'student_email{i}' if j == 1 else f'student_roll_number{i}' if j == 2 else f'marks_of_{i}' if j == 3 else f'b_form_name{i}' if j == 4 else f'student_class' if j == 5 else f'subject'
                tuple_attandance.append(student_restult.get(key))
            student_marks.append(tuple_attandance)
        
        print("The resutlls sis sd = " ,student_marks)

        cheek = obj.send_student_marks_of_db(student_marks , result_type_data)
        if cheek:
            flash((f"The result of {student_restult['subject']} will Upload Successfully !!!! " , 'result_uploaded'))
            return render_template('teacher_URLs/teacher_dashboard.html' , data = data )
        
        flash((f"The result of {student_restult['subject']} will Not Upload  !!!! " , 'result_will_not_uploaded'))
        
        return render_template('teacher_URLs/teacher_dashboard.html' , data = data )


    
@app.route('/teacher/delete_dairy' , methods=["GET", "POST" , "DELETE"] )
@login_required('teacher')
def delete_dairy():
    data = request.args.get('data')
    result = str(data) 
    result_dict = eval(result)  # or use json.loads(result) for JSON parsing
    if request.method == "GET":
        dariy_data = obj.take_teacher_dariy_for_db_for_delete(result_dict)
        return render_template('teacher_URLs/delete_dairy.html', dariy_data=dariy_data, data=result_dict)
    if request.method == "POST":
        result = request.form.get('delete_information')
        result_dict = str(result) 
        delete_dairy_information = eval(result_dict)
        print("The data is == " , delete_dairy_information)
        print("Thsi is working then good =  = = " , delete_dairy_information[1])
        
        obj.delete_dariy_for_db_which_teacher_select(delete_dairy_information)
        
        return render_template('teacher_URLs/teacher_dashboard.html',  data=data)
        

    


@app.route('/teacher/delete_notification_teacher', methods=["GET", "POST"])
@login_required('teacher')
def delete_notification_teacher():
    data = request.args.get('data')
    result = str(data) 
    result_dict = eval(result)
    print("This is teacher name" , result_dict)
    

    if request.method == 'GET':
        notification_data = obj.take_teacher_notification_of_class_for_db_for_delete(result_dict)
        print("This is notification_data =", notification_data)
        if notification_data == False:
            flash(("You will Not send any Notification To you class !!!" , 'no_notification_send_by_teacher_to_student'))
            return render_template('teacher_URLs/teacher_dashboard.html' ,  data = result_dict)   
        else:
            return render_template('teacher_URLs/delete_notification_teacher.html', notification_data=notification_data , data = result_dict)
    if request.method == 'POST':
        result = request.form.get('delete_notification')
        email = request.form.to_dict()
        result_dict = str(result) 
        delete_notification = eval(result_dict)
        print("Teh delete not sdf  = = = = =ee3=  = " , delete_notification)
        obj.delete_selected_notification_form_data(delete_notification)
        print("Now its endsss")
        flash(("You will Delete the Massage Successfully !!!" , 'delete_notification_principal'))
        return render_template('teacher_URLs/teacher_dashboard.html' ,  data = data)        
        
        
