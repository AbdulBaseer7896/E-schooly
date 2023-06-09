from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash



def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/student/dashboard' , methods=["GET", "POST"])
@login_required('student')
def student_dashboard():
    data = request.args.get('data')
    # Functionality for student dashboard
    flash(('Dear student Welcome to Iqra-E-Schooly !!! You Successfully Login !!!' , 'student_login'))
    return render_template("student_URLs/student_dashboard.html", data = data)

@app.route('/teacher/dashboard')
@login_required('teacher')
def teacher_dashboard():
    data = request.args.get('data')
    # Functionality for teacher dashboard
    flash(('Dear Teacher Welcome to Iqra-E-Schooly !!! You Successfully Login !!!' , 'teacher_login'))
    return render_template("teacher_URLs/teacher_dashboard.html" , data= data)

@app.route('/principal/dashboard')
@login_required('principal')
def principal_dashboard():
    # Functionality for teacher dashboard
    data = request.args.get('data')
    flash(('Dear Principal Welcome to Iqra-E-Schooly !!! You Successfully Login !!!' , 'principal_login'))
    return render_template('principal_URLs/principal_dashboard.html' , data = data)

@app.route('/teacher_admin/dashboard')
@login_required('teacher_admin')
def teacher_admin_dashboard():
    # Functionality for admin dashboard
    data = request.args.get('data')
    print("This is data = " , data)
    flash(('Dear Teacher Admin Welcome to Iqra-E-Schooly !!! You Successfully Login !!!' , 'teacher_admin_login'))
    return render_template('/teacher_admin_URLs/teacher_admin_dashboard.html' , data = data)

@app.route('/school_admin/student')
@login_required('school_admin')
def school_admin_dashboard():
    flash(('Dear School Admin Welcome to Iqra-E-Schooly !!! You Successfully Login !!!' , 'school_admin_login'))
    return render_template("school_admin_URLs/school_admin_dashboard.html")


@app.route('/staff/student')
@login_required('staff')
def staff_dashboard():
    return 'welcom , staff'

