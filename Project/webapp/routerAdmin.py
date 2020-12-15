import json
import datetime

from flask import request, flash, redirect, url_for, render_template, jsonify, session
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
        if utils.check_hometeam_stadium(id_hometeam=hometeam, id_awayteam=awayteam, id_group=group_id):
            if utils.create_match(datetime=datetime, group_id=group_id, hometeam_id=hometeam, awayteam_id=awayteam,
                                  stadium_id=hometeam):
                flash("Tạo vòng đấu thành công!", category="success")
            else:
                flash("Tạo vòng đấu không thành công!", category="error")
            return redirect(url_for('match_admin'))
        else:
            flash("Không thể tạo trận đấu!! Đội nhà đã gặp đội khách tại sân nhà! Yêu cầu tạo lại")
    params['listgroup'] = models.Groups.query.all()
    params['listmatch'] = models.Match.query.all()
    params['listround'] = models.Round.query.all()
    params['listteam'] = models.Team.query.all()
    params['result'] = models.Result
    return render_template('admin/models/match/list.html', params=params)

@app.route('/admin/match/delete', methods=['POST'])
@decorate.login_required_Admin
def delete_match():
    match_id = request.json.get('idmatch')
    print(session)
    if match_id and utils.delete_match(match_id):
         flash('Xóa match thành công')
         return jsonify({
             'statuss': 200,
         })
    return jsonify({
        'statuss': 400,
    })

@app.route('/admin/result/list', methods=['GET','POST'])
@decorate.login_required_Admin
def resultlist():
    pass

@app.route('/admin/match/get_stadium', methods=['GET', 'POST'])
@decorate.login_required_Admin
def get_stadium():
    data = request.json
    hometeam  = None
    try:
        if data:
            hometeam = models.Team.query.get(data.get('hometeam'))
    except Exception as e:
        print('Error get_stadium', e)

    return jsonify({
        "hometeam": {
            "stadium": " - ".join([hometeam.name, hometeam.stadium or ""]) or None
        },
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
        flash(roundname + numberteamin + '     ' + numberteamout)
        if utils.create_round(roundname=roundname, numberteamin=int(numberteamin), numberteamout=int(numberteamout),
                              format=format):
            flash("Tạo vòng đấu thành công!", category="success")
        else:
            flash("Tạo vòng đấu không thành công!", category="error")

    params['listround'] = models.Round.query.all()
    params['listgroup'] = models.Groups
    return render_template('admin/models/round/list.html', params=params)

@app.route('/admin/round/delete', methods=['POST'])
def delete_round():
    round_id = request.json.get('idround')
    print(round_id)
    if round_id and utils.delete_round(round_id):
         flash('Xóa group thành công')
         return jsonify({
             'statuss': 200,
         })
    return jsonify({
        'statuss': 400,
    })

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
    params['listmatch'] = models.Match
    return render_template('admin/models/group/list.html', params=params)

@app.route('/admin/group/delete', methods=['POST'])
def delete_group():
    group_id = request.json.get('idgroup')
    print(group_id)
    if group_id and utils.delete_group(group_id):
         flash('Xóa group thành công')
         return jsonify({
             'statuss': 200,
         })
    return jsonify({
        'statuss': 400,
    })

