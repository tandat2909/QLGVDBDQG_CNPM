import json
import datetime

from flask import request, flash, redirect, url_for, render_template, jsonify
from flask_login import logout_user, login_user, current_user

from webapp import models, Forms, utils, app, decorate, config_main, SentEmail,EMethods



@app.route('/admin')
@app.route('/admin/')
@decorate.login_required_Admin
def index_admin():
    pargams = {
        'title': 'Home'
    }
    return render_template('admin/index.html', params=pargams)


@app.route('/admin/logout')
def logout_admin():
    logout_user()
    return redirect('/admin')


@app.route("/admin/login", methods=["GET", "POST"])
def login_admin():
    """
    login cho trang admin
    :return:
    """
    logout_user()
    form = Forms.LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        next_url = request.args.get('next')
        login_info = json.loads(request.form.get("info_connect"))
        # flash('login admin: ' + user.password +str(user.active) + "-"+ str(models.EActive.Active.value) + "-"+ str(user.role)+"-"+ str(models.Role.admin))
        if user and user.active == models.EActive.Active.value and user.role == models.Role.admin:
            login_user(user=user, remember=True, duration=datetime.timedelta(hours=1))
            SentEmail.sent_mail_login(current_user, login_info)
            flash("Login Success", category='success')
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index_admin'))
        logout_user()
        if user:
            flash("Invalid username or password", category='error')
            user = None

    return render_template('login.html', form=form, title='Login Admin', action='login_admin')


@app.route('/admin/accounts', methods=['POST', 'GET'])
@decorate.login_required_Admin
def accounts():
    """
    hiển thị tất cả user trừ tài khoản admin hiện tại
    :return:
    """
    params = {
        'title': "Accounts",
        'nav_team': 'active',
        'tabs_list': ['active', 'true'],
        'tabs_create': ['', 'false'],
    }
    if request.method == 'POST':
        if request.args.get('action').upper() == EMethods.create.value:
            form = request.form
            try:
                if utils.check_form_register_account(form):
                    if utils.create_account(form=form):
                        flash('Success Create account ', category='success')
                        return redirect(url_for('account_list'))
                    else:
                        flash('Error Create Account ', category='error')
            except ValueError as e:
                flash(str(e), category='error')
                params['form'] = form
                params['tabs_list'] = ['', 'false']
                params['tabs_create'] = ['active', 'true']
            except Exception as e:
                print('register error:', e)

        if request.args.get('action') == 'sent_account':
            idteam = request.json.get('idt')
            print(idteam)
            if idteam and SentEmail.sent_account_to_mail(idteam):
                return jsonify({
                    'status':200
                })
            return jsonify({
                'status':400
            })
    listuser = models.Team.query.filter(models.Team.id != current_user.id)
    params['listuser'] = listuser
    return render_template('admin/UserList.html', params=params)

@app.route('/admin/lock/user', methods=["POST"])
@decorate.login_required_Admin
def lock_user():
    """

    :return: trả về thông báo xóa thành công hay không

    """

    try:
        if current_user.role == models.Role.admin:
            data = request.json
            lock = data.get('lock')
            user_id = data.get("idu")

            if lock == 'lock':
                if utils.lock_account(current_user=current_user, user_id=user_id, lock=True):
                    return jsonify({
                        "status": 200,
                        "data": "UnLock"
                    })
            if lock == 'unlock':
                if utils.lock_account(current_user=current_user, user_id=user_id, lock=False):
                    return jsonify({
                        "status": 200,
                        "data": "Lock"
                    })
        raise
    except:
        return jsonify({
            "status": 404,
            "data": "Error"
        })


@app.route('/admin/list/team', methods=['GET', 'POST'])
@decorate.login_required_Admin
def listteam():
    params = {
        'title': 'Team',
        'nav_team': 'active',
    }
    # creat Team
    if request.method == "POST":
        pass
    return render_template('admin/models/team/list.html')


@app.route('/admin/list/match/', methods=['GET', 'POST'])
@decorate.login_required_Admin
def match_admin():
    params = {
        'title': 'Match',
        'nav_match': 'active',
    }
    # creat Team
    if request.method == "POST":
        pass

    params['listmatch'] = models.Match.query.all()
    return render_template('admin/models/match/list.html', params=params)
