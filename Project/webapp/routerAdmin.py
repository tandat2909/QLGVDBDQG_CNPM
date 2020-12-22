import json
import datetime

from flask import request, flash, redirect, url_for, render_template, jsonify
from flask_login import logout_user, login_user, current_user

from webapp import models, Forms, utils, app, decorate, SentEmail,EMethods
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


@app.route('/admin/match/list/', methods=['GET', 'POST'])
@decorate.login_required_Admin
def match_admin():
    params = {
        'title': 'Match',
        'nav_match': 'active',
    }
    # creat Team
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
    params['typegoals'] = models.TypeGoals.query.all()
    return render_template('admin/models/match/list.html', params=params)

@app.route('/admin/match/delete', methods=['POST'])
@decorate.login_required_Admin
def delete_match():
    match_id = request.json.get('idmatch')
    if match_id and utils.delete_match(match_id):
        flash('Xóa trận đấu thành công',category='success')
        return jsonify({
            'statuss': 200,
        })
    flash('Lỗi xóa trận đấu', category='success')
    return jsonify({
        'statuss': 400,
    })


@app.route('/admin/results', methods=['GET', 'POST'])
@decorate.login_required_Admin
def results():
    if request.method == EMethods.post.value:
        if request.args.get("action").upper() == EMethods.edit.value:
            form = request.form
            print(form.to_dict())
            print(form.getlist('awaygoalplayer'))
            print(request.form_data_parser_class.__dict__)
        if request.args.get("action").upper() == EMethods.get.value:
            try:
                hometeamid = request.json.get('hometeamid')
                awayteamid = request.json.get('awayteamid')
                matchid = request.json.get('matchid')
                playerhome = utils.get_list_player(hometeamid)
                playeraway = utils.get_list_player(awayteamid)
                match = models.Match.query.get(matchid)
                # lấy kết quả của trận đấu get result => get typegoal => player
                # lấy goal => result , player id ,
                html_option_playerhome = ""
                html_option_playeraway = ""
                for i in playerhome:
                    html_option_playerhome += "<option value='%s'>%s</option>" %(i.id,i.name)
                for i in playeraway:
                    html_option_playeraway += "<option value='%s'>%s</option>" % (i.id, i.name)
                resulthome,resultaway = utils.get_result_for_writematch(matchid)
                return jsonify({
                    'data':{
                        'home':{
                            'player':html_option_playerhome,
                            'result': resulthome
                        },
                        'away': {
                            'player': html_option_playerhome,
                            'result': resultaway
                        },
                    }
                })
            except Exception as e:
                print("Error result get list player",e)
                return jsonify({
                    'data':'error'
                })



    params = {
        'title': "Kết quả",
        'nav_result': 'active',
        'results': models.Result.query.all()
    }

    return render_template('admin/result.html', params=params)


@app.route('/admin/match/get_stadium', methods=['GET', 'POST'])
@decorate.login_required_Admin
def get_stadium():
    data = request.json
    hometeam = None
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

@app.route('/admin/player/list/')
@decorate.login_required_Admin
def listplayer():
    params = {
        'title': 'Player',
        'nav_player': 'active',
    }
    params["teams"] = models.Team.query.all()
    return render_template('admin/models/player/list.html', params=params)

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
@app.route('/admin/group/addteam', methods=['POST', 'GET'])
def add_team():
    params = {
        'title': 'Addteam',
        'nav_group': 'active',
    }
    if request.method == "POST":
        team = request.form.getlist('checkbox')
        group = request.form.get('group_id')
        try:
            if utils.add_team_in_group(team,group):
                flash("Thêm team vào bảng thành công", category="success")
        except ValueError as e:
            flash(e,category="error")
        except Exception as e:
            print('Lỗi add team', e)
    params['listgroup'] = models.Groups.query.all()
    params['teams'] = utils.get_team_not_in_group()
    return render_template('admin/models/group/addteam.html', params=params)


@app.route('/admin/changeconfig', methods=["GET", "POST"])
@decorate.login_required_Admin
def changeconfig():
    if request.method == EMethods.post.value:
        try:
            utils.check_change_config(request.form)
            if utils.change_config(request.form):
                flash("Lưu thay đổi thành công", category='success')
                return redirect(url_for('changeconfig'))
            else:
                flash("Lỗi thay đổi quy định")
        except ValueError as e:
            flash("Lỗi lưu quy định: " + str(e), category='error')
        except Exception as e:
            print("Lỗi change config", e)

    params = {
        'title': 'Thay đổi quy định',
        'config': models.Config.query.first(),
    }
    return render_template('admin/config.html', params=params)

@app.route('/admin/typegoal',  methods=['GET', 'POST'])
@decorate.login_required_Admin
def typeGoal():
    if request.method == EMethods.post.value:
        typeGoal = request.form.get('typeGoal')
        if typeGoal and utils.create_type_goal(typeGoal):
            flash('Thêm loại bàn thắng thành công',category='success')
        else:
            flash('Lỗi thêm loại bàn thắng',category='error')
        return redirect(url_for('typeGoal'))

    params = {
        'title': 'loại bàn thắng',
        'typeGoal': models.TypeGoals.query.all()
    }
    return render_template('admin/TypeGoal.html',params=params)


# todo xóa round,result,match,group,gold xóa nguyên round và các trận liên quan
# todo xuất list player
# todo trang result thêm xóa
# todo trang edit config
# todo type goal thêm xóa
