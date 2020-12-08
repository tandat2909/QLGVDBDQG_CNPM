import json
import datetime

from flask import request, flash, redirect, url_for, render_template
from flask_login import logout_user, login_user, current_user

from webapp import models, Forms, utils, app,decorate



@app.route('/user/')
@decorate.login_required_user
def index_user():
    params = {
        'title': 'Home'
    }
    return render_template('user/index.html')
@app.route('/user/logout')
def logout_user():
    logout_user()
    return redirect('/user')

@app.route("/user/login", methods=["GET", "POST"])
def login_us():
    """
    login cho trang user
    :return:
    """
    form = Forms.LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        next_url = request.args.get('next')
        login_info = json.loads(request.form.get("info_connect"))
        if user and user.active == models.EActive.Active.value and user.role == models.Role.manager:
            flash("Login Success", category='success')
            login_user(user=user, duration=datetime.timedelta(hours=1), remember=True)
            utils.sent_mail_login(current_user, login_info)
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index_user'))

        logout_user()
        if user:
            flash("Invalid username or password", category='error')
            user = None
    return render_template('login.html', form=form, title="Login User", action="login_us")
