from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for



def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/student/dashboard')
@login_required('student')
def student_dashboard():
    # Functionality for student dashboard
    return 'Welcome, student!'

@app.route('/teacher/dashboard')
@login_required('teacher')
def teacher_dashboard():
    # Functionality for teacher dashboard
    return 'Welcome, teacher!'

@app.route('/principal/dashboard')
@login_required('principal')
def principal_dashboard():
    # Functionality for teacher dashboard
    return 'Welcome, principal!'

@app.route('/teacher_admin/dashboard')
@login_required('teacher_admin')
def teacher_admin_dashboard():
    # Functionality for admin dashboard
    return 'Welcome, teacher-admin!'

@app.route('/school_admin/student')
@login_required('shool_admin')
def school_admin_dashboard():
    return 'welcom , school admin'


@app.route('/staff/student')
@login_required('staff')
def staff_dashboard():
    return 'welcom , staff'