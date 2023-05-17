from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request
from model.student_model import student_model

obj = student_model()

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator



@app.route('/student/profile')
@login_required('student')
def student_profile():
    # Functionality for teacher dashboard
    return render_template('student_URLs/student_profile.html')
