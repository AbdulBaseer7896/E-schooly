from flask import Flask , render_template , request
from model.user_model import user_model
app = Flask(__name__)
app.secret_key = "your_secret_key"
obj = user_model()

@app.route("/")
def hello_world():
    cheek = obj.get_iqra_posts_form_db()
    return render_template('index.html' , posts = cheek)

from controller import *


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)