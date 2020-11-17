from webapp import app,models,db,login
from flask import request,render_template,redirect,url_for,abort,current_app
from flask_login import current_user,login_user,logout_user,login_required,login_url

@app.route('/')
def home():
    return render_template("index.html")



@login.user_loader
def get_user(id):
    return models.User.query.get(id)
if __name__=='__main__':

    app.run(debug=True)
