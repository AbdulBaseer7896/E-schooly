from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request ,flash





@app.route('/school_admin/Iqra_image_gallery' , methods=["GET", "POST"])
def Iqra_image_gallery():
    if request.method == "GET":
        # flash("Welcome to the website!", "success")
        return render_template("Iqra_image_gallery.html")
    
    # elif request.method == 'POST':
    #     data = request.form.to_dict()
    #     result = obj.search_student_admission_data(data)
    #     print("This is resut = " , result)
    #     return render_template("school_admin_URLs/student_admission.html" , data = result)
        
    # return render_template("school_admin_URLs/update_admission_data.html")

