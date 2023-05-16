from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request
from model.school_admin_model import user_model

obj = user_model()

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
    # Functionality for student dashboard
    if request.method == "GET":
        # if the request is a GET request, render the login form
        # flash("Welcome to the website!", "success")
        return render_template("school_admin_URLs/student_admission.html")
    
    elif request.method == 'POST':
        print("Data is = ")
        data = request.form.to_dict()
        print(data)
        obj.student_admission_data(data)
    return render_template("school_admin_URLs/student_admission.html")
