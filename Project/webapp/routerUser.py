import json
import datetime

from flask import request, flash, redirect, url_for, render_template, abort
from flask_login import logout_user, login_user, current_user

from webapp import models, Forms, utils, app, decorate, SentEmail, EMethods


@app.route('/user/')
@decorate.login_required_user
def index_user():
    params = {
        'title': 'Dashboard',
        'nav_dashboard': 'active'
    }
    return render_template('user/index.html', params=params)


@app.route('/user/logout')
@decorate.login_required_user
def logout_user():
    logout_user()
    return redirect(url_for('login_us'))


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
            login_user(user=user, duration=datetime.timedelta(hours=1), remember=True)
            if not user.invalid:
                return redirect(url_for('changepwfirst'))
            flash("Login Success", category='success')
            SentEmail.sent_mail_login(current_user, login_info)
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index_user'))

        logout_user()
        if user:
            flash("Invalid username or password", category='error')
            user = None
    return render_template('login.html', form=form, title="Login User", action="login_us")


@app.route("/user/players")
@decorate.login_required_user
def players():
    params = {
        'title': 'Dang sách cầu thủ',
        'nav_player': 'active'
    }
    params['lsplayer'] = utils.get_list_player(teamid=current_user.id)
    return render_template('user/player.html', params=params)

@app.route("/user/players/createplayer")
@decorate.login_required_user
def creatPlayer():
    params = {
        'title': 'Thêm cầu thủ',
        'nav_player': 'active',
        'positions':models.Position.query.all()
    }

    if request.method == "POST":
        pass

    return render_template('user/createplayer.html',params=params)