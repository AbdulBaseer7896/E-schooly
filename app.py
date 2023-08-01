from flask import Flask , render_template , request
from sqlalchemy.exc import OperationalError
from model.user_model import user_model
app = Flask(__name__)
app.secret_key = "your_secret_key"
obj = user_model()

@app.route("/")
def hello_world():
    cheek = obj.get_iqra_posts_form_db()
    return render_template('index.html' , posts = cheek)

from controller import *

@app.errorhandler(OperationalError)
def handle_operational_error(error):
    app.logger.error(f"OperationalError: {str(error)}")
    return render_template('error.html', message="An error occurred while processing your request."), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)