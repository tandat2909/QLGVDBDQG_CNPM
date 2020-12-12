import json
import datetime

from flask import request, flash, redirect, url_for, render_template, jsonify
from flask_login import logout_user, login_user, current_user

from webapp import models, Forms, utils, app, decorate, config_main


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
            utils.sent_mail_login(current_user, login_info)
            flash("Login Success", category='success')
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index_admin'))
        logout_user()
        if user:
            flash("Invalid username or password", category='error')
            user = None

    return render_template('login.html', form=form, title='Login Admin', action='login_admin')


@app.route('/admin/accountlist')
@decorate.login_required_Admin
def account_list():
    """
    hiển thị tất cả user trừ tài khoản admin hiện tại
    :return:
    """
    params = {
        'title': "Accounts",
        'nav_team': 'active',

    }

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


@app.route('/admin/match/list/', methods=['GET', 'POST'])
@decorate.login_required_Admin
def match_admin():
    params = {
        'title': 'Match',
        'nav_match': 'active',
    }
    if request.method == "POST":
        datetime = request.form.get('datetime')
        group_id = request.form.get('group_id')
        hometeam = request.form.get('hometeam')
        awayteam = request.form.get('awayteam')
        stadium = request.form.get('stadium')
        if utils.create_match(datetime=datetime, group_id=group_id,hometeam_id=hometeam, awayteam_id=awayteam,stadium_id=stadium):
            flash("Tạo vòng đấu thành công!", category="success")
        else:
            flash("Tạo vòng đấu không thành công!", category="error")
    params['listgroup'] = models.Groups.query.all()
    params['listmatch'] = models.Match.query.all()
    params['listround'] = models.Round.query.all()
    params['listteam'] = models.Team.query.all()
    return render_template('admin/models/match/list.html', params=params)


@app.route('/admin/match/get_stadium', methods=['GET', 'POST'])
@decorate.login_required_Admin
def get_stadium():
    data = request.json
    hometeam = awayteam = None
    try:
        if data:
            hometeam = models.Team.query.get(data.get('hometeam'))
            awayteam = models.Team.query.get(data.get('awayteam'))
    except Exception as e:
        print('Error get_stadium', e)

    return jsonify({
        "hometeam": {
            "id": str(hometeam.id) or None,
            "stadium": " - ".join([hometeam.name ,hometeam.stadium or ""]) or None
        },
        "awayteam": {
            "id": str(awayteam.id) or None,
            "stadium": " - ".join([awayteam.name ,awayteam.stadium or ""]) or None
        }
    })


@app.route('/admin/create/account', methods=['POST'])
@decorate.login_required_Admin
def createaccount():
    form = request.form
    s = models.Team()
    return redirect(url_for('account_list'))


@app.route('/admin/list/round/', methods=['GET', 'POST'])
@decorate.login_required_Admin
def listround():
    params = {
        'title': 'Round',
        'nav_round': 'active',
    }
    if request.method == "POST":
        roundname = request.form.get('roundname')
        numberteamin = request.form.get('numberteamin')
        numberteamout = request.form.get('numberteamout')
        format = request.form.get('format')
        if utils.create_round(roundname=roundname, numberteamin=int(numberteamin), numberteamout=int(numberteamout),
                              format=format):
            flash("Tạo vòng đấu thành công!", category="success")

    params['listround'] = models.Round.query.all()
    return render_template('admin/models/round/list.html', params=params)


@app.route('/admin/list/group/', methods=['GET', 'POST'])
@decorate.login_required_Admin
def listgroup():
    params = {
        'title': 'Group',
        'nav_group': 'active',
    }
    if request.method == "POST":
        groupname = request.form.get('groupname')
        numberteamin = request.form.get('numberteamin')
        numberteamout = request.form.get('numberteamout')
        round_id = request.form.get('round_id')

        if utils.create_group(groupname=groupname, numberteamin=int(numberteamin), numberteamout=int(numberteamout),
                              round_id=round_id):
            flash("Tạo bảng đấu thành công!", category="success")
        else:
            flash("Tạo bảng đấu không thành công!", category="error")

    params['listgroup'] = models.Groups.query.all()
    params['listround'] = models.Round.query.all()
    return render_template('admin/models/group/list.html', params=params)
