from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request ,flash
from model.school_admin_model import school_admin_models

obj = school_admin_models()

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator



@app.route('/school_admin/student admission' , methods=["GET", "POST"])
@login_required('school_admin')
def student_admission():
    data = [('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')]
    if request.method == "GET":
        # flash("Welcome to the website!", "success")
        print("Thisj ofiasj ofjsdi oif  &&&&&&& = " ,data)
        return render_template("school_admin_URLs/student_admission.html" ,  data = data )
    
    elif request.method == 'POST':
        dataa = request.form.to_dict()
        student_id_for_updatae = dataa['student_email']
        # image_name = dataa['student_image']
        image_file = request.files['student_image']
        folder_name = 'admission_student_images'
        if image_file and image_file.filename:
            print("Thisj ijfid if image _ file = = " , image_file)
            image_path = obj.stored_image_in_file_and_send_path_in_db(image_file , folder_name)
        else:
            print("There is not image at alll ija ")
            image_path = ""
        # print("The student name = " , dataa['])
        print("THis is image path as you see = " , image_path)
        cheek = obj.student_admission_data(dataa , image_path , student_id_for_updatae )
        try:
            if cheek[0][2] == 'student':
                flash((f"The B-Form Number You Entered Is Already Exist !!! So Visit The  Student Registration Number = [ {cheek[0][1]} ] !!! " , "search_student_cnic"))
                return  render_template("school_admin_URLs/update_admission_data.html")
            if cheek[0][2] == 'teacher':
                flash((f"The CNIC Number You Entered Is Already Exist !!! So Visit The Teacher ID Number = [ {cheek[0][1]} ] !!! " , "search_teacher_cnic"))
                return  render_template("school_admin_URLs/update_teacher_data.html")
        except:
            if  cheek:
                flash(('New Student Information Upload Successfully !!!' , 'student_admission_done'))
                return render_template("school_admin_URLs/student_admission.html" ,  data = data )


@app.route('/school_admin/update_admission_data' , methods=["GET", "POST"])
@login_required('school_admin')
def update_admission_data():
    if request.method == "GET":
        # flash("Welcome to the website!", "success")
        return render_template("school_admin_URLs/update_admission_data.html")
    
    elif request.method == 'POST':
        data = request.form.to_dict()
        result = obj.search_student_admission_data(data)
        print("This is resut = " , result)
        return render_template("school_admin_URLs/student_admission.html" , data = result)
        
    return render_template("school_admin_URLs/update_admission_data.html")




@app.route('/school_admin/Teacher_Joining' , methods=["GET", "POST"])
@login_required('school_admin')
def teacher_joining_information():
    data = [('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')]
    if request.method == "GET":
        # flash("Welcome to the website!", "success")
        return render_template("school_admin_URLs/teacher_joining.html" ,  data = data )
    
    elif request.method == 'POST':
        dataa = request.form.to_dict()
        teacher_id_for_update = dataa['teacher_id']
        
        image_file = request.files['teacher_image']
        folder_name = 'jonning_teacher_images'
        if image_file and image_file.filename:
            print("Thisj ijfid if image _ file = = " , image_file)
            image_path = obj.stored_image_in_file_and_send_path_in_db(image_file , folder_name)
        else:
            print("There is not image at alll ija ")
            image_path = ""
        if image_path:
            # print("The student name = " , dataa['])
            print("THis is image path as you see = " , image_path)
        cheek = obj.teacher_joining_information_to_db(dataa ,image_path , teacher_id_for_update)
        
        try:
            if cheek[0][2] == 'student':
                flash((f"The B-Form Number You Entered Is Already Exist !!! So Visit The  Student Registration Number = [ {cheek[0][1]} ] !!! " , "search_student_cnic"))
                return  render_template("school_admin_URLs/update_admission_data.html")
            if cheek[0][2] == 'teacher':
                flash((f"The CNIC Number You Entered Is Already Exist !!! So Visit The Teacher ID Number = [ {cheek[0][1]} ] !!! " , "search_teacher_cnic"))
                return  render_template("school_admin_URLs/update_teacher_data.html")
        except:
            if  cheek:
                flash(('New Teacher Information Upload Successfully !!!' , 'teacher_information_upload'))
                return render_template("school_admin_URLs/teacher_joining.html" ,  data = data )

     


@app.route('/school_admin/update_teacher_data' , methods=["GET", "POST"])
@login_required('school_admin')
def update_teacher_data():
    if request.method == "GET":
        # flash("Welcome to the website!", "success")
        return render_template("school_admin_URLs/update_teacher_data.html")
    
    elif request.method == 'POST':
        data = request.form.to_dict()
        result = obj.search_teacher_data(data)
        print("This is resut = " , result)
        return render_template("school_admin_URLs/teacher_joining.html" , data = result)
        
    return render_template("school_admin_URLs/update_teacher_data.html")




@app.route('/school_admin/seach_student_result' , methods=["GET", "POST"])
@app.route('/school_admin/display_student_result' , methods=["GET", "POST"])
@login_required('school_admin')
def seach_student_result():
    if request.method == "GET":
        return render_template('school_admin_URLs/seach_student_result.html')
    if request.method =="POST":
        data = request.form.to_dict()
        print("This ijsa fi = " , data)
        result = obj.search_student_admission_data(data)
        print("This is isfoands g g )))))))))) = " , result)
        student_name =  result[0][0]
    
        marks_result = obj.take_student_result_data(student_name)
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

        return render_template('school_admin_URLs/display_student_result.html', result_data=marks_result, data=data, grouped_data=updated_grouped_data, combined_data=combined_data)

    
    
@app.route('/school_admin/forget_password' , methods=["GET", "POST"])
@login_required('school_admin')
def forget_password_by_admin():
    if request.method == "GET":
        flash(("Do Not Share User Personal Information to Any Body !!! Except User Parents !!!" , 'forget_password_warrning'))
        return render_template('school_admin_URLs/forget_password_by_admin.html')
    elif request.method == 'POST':
        data = request.form.to_dict()
        print("This is data = = " , data)
        result = obj.search_user_data_for_forger_password(data)
        print("The result is si si =  = " , result)
        if result:
                password_data = obj.search_user_passwrod(result)
                print("This is password data is = == = " , password_data)
                return render_template('school_admin_URLs/display_password.html' , data = data , password_data = password_data , result = result)
        else:
            flash(("That user could not exit !!! Recheck the User-type And Search Information !!!" , 'no_user_found_for_forget_password'))
            return render_template("school_admin_URLs/forget_password_by_admin.html" , data = data)
    
    


@app.route('/principal/check_student_attandance', methods=["GET", "POST"])
@login_required('school_admin')
def check_student_attandance():
    if request.method == "GET":
        attendance = obj.take_student_attandance_for_db()
        total_attendance = obj.take_total_number_of_working_days_of_student()
        
        return render_template('school_admin_URLs/student_attandance.html', attendance=attendance, total_attendance=total_attendance)



# [('daimraza-3-3-10@iqra.edu', '3710471513456', 'Abdula Khan', '3701471623456', 'Muslim', 'Male', 'Class 10', datetime.date(2023, 5, 24), '', '34567892345', 'Class 9', 'A-', 'Math , science , Data science , Data Base', 'Abc home pindi ghen, Attock ,pakistan', 'Iqra education school pindi ghed , Attock', 'Abdula Khan', '34567823456', '3', 'Daim Raza', '3', 0)]
# [('M Hamza', '1', 'mhamza-1-4-9@iqra.edu', 'Final Exam', 'Math', 50, 100, datetime.date(2023, 5, 19)), ('M Hamza', '1', 'mhamza-1-4-9@iqra.edu', 'Final Exam', 'Urdu Book', 30, 100, datetime.date(2023, 5, 19)), ('M Hamza', '1', 'mhamza-1-4-9@iqra.edu', 'Mid Exam', 'English Book', 80, 100, datetime.date(2023, 5, 19))]