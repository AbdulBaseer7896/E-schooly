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


        return render_template("school_admin_URLs/student_admission.html" ,  data = data )
    
    elif request.method == 'POST':
        dataa = request.form.to_dict()
        # print("The student name = " , dataa['student_name'])
        obj.student_admission_data(dataa)
        flash(('New Student Information Upload Successfully !!!' , 'student_admission_done'))
        return render_template("school_admin_URLs/student_admission.html" ,  data = data)


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
        obj.teacher_joining_information(dataa)
        flash(('New Teacher Information Upload Successfully !!!' , 'teacher_information_upload'))
        return render_template("school_admin_URLs/teacher_joining.html" ,  data = data)




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

