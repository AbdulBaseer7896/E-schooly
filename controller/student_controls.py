from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request
from model.student_model import student_model
from model.school_admin_model import school_admin_models
import datetime

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
    data = request.args.get('data')
    result = str(data) 
    # Parse the string representation of the dictionary back to a dictionary object
    result_dict = eval(result)
    result = obj.take_student_profile_data(result_dict)
    return render_template('student_URLs/student_profile.html' , data = result )
