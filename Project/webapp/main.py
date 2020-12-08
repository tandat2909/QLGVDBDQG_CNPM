from webapp import app,login,models
from flask import request,render_template,redirect,url_for,abort,current_app,flash
from flask_login import current_user,login_user,logout_user,login_required,login_url,AnonymousUserMixin
from webapp.admin import *
@app.route('/')
def home():
    params = {
        'title':'Home'
    }
    return render_template("home/base.html",params=params)


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/admin')
app.route("/admin/login",methods=['post'])
def login_admin():
    pass
#   if request.method=="POST":
#       username = request.form.get('username')
#       password = request.form.get('password')
#       remember = request.form.get('remember')
#       user = models.User.query.filter(models.User.username == username,models.User.password == password ,models.User.active == True).first()
#       if user:
#           if user.role == models.Role.admin:
#               login_user(user,remember)
#               flash('Đăng nhập thành công')
#               return redirect('/admin')
#           else:
#               flash("Cần đăng nhập tài khoản admin",category='error')
#       else:
#           flash("Tài khoản mật khẩu không đúng",category='error')
#   return redirect('/admin')

@login.user_loader
def get_user(id):
    return models.Team.query.get(id)
if __name__=='__main__':

    app.run(debug=True)
