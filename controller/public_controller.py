from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request ,flash
from model.user_model import user_model

obj = user_model()



@app.route('/Iqra_image_gallery' , methods=["GET", "POST"])
def Iqra_image_gallery():
    if request.method == "GET":
        cheek = obj.get_gallery_images_form_db()
        print(cheek)
        # flash("Welcome to the website!", "success")
        return render_template("Iqra_image_gallery.html" , images = cheek)
    
    
    
@app.route('/Iqra_posts' , methods=["GET", "POST"])
def Iqra_posts():
    if request.method == "GET":
        cheek = obj.get_iqra_posts_form_db()
        print(cheek)
        # flash("Welcome to the website!", "success")
        return render_template("index.html" , posts = cheek)
    




    
