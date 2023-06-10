from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request ,flash



# not is used
# @app.route('/' , methods=["GET", "POST"])
# def hello_world__():
#     return render_template('index.html')

