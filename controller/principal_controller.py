from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request
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
        return render_template('principal_URLs/principal_dashboard.html')