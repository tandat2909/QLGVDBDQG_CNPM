import json
import datetime
import os

from flask import request, flash, redirect, url_for, render_template, abort, jsonify
from flask_login import logout_user, login_user, current_user,login_required

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
@login_required
def logout_usr():
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


@app.route("/user/players", methods=["GET", "POST"])
@decorate.login_required_user
def players():
    params = {
        'title': 'Danh sách thành viên',
        'nav_player': 'active',
        'positions': models.Position.query.all(),
        'genders': models.EGender,
        'tyepeplayer': models.ETyEpePlayer,
    }

    if request.method == EMethods.post.value:

        if request.args.get("action").upper() == EMethods.delete.value:
            playerid = request.json.get("playerid")
            if utils.delete_player(playerid=playerid):
                return jsonify({"data": True})
            return jsonify({"data": False})
        if request.args.get("action").upper() == EMethods.get.value:
            try:
                playerid = request.json.get("playerid")
                a = models.Player.query.get(playerid)
                return jsonify({
                    "firstname": a.firstname,
                    "lastname": a.lastname,
                    "position": str(a.position_id),
                    "note": a.note,
                    "typeplayer": a.typeplayer.name,
                    "birthdate": str(a.birthdate.strftime("%Y-%m-%d")),
                    "gender": a.gender.name,
                    "scorecount": a.scorecount,
                    "nationality": a.nationality,
                    "number":a.number
                })
            except Exception as e:
                print("Error get player:",e)
                return jsonify({"data":"error"})
        if request.args.get("action").upper() == EMethods.edit.value:
            try:
                if utils.check_form_add_player(teamid=current_user.id, form=request.form):
                    avatars = request.files["avatar"]
                    avatar_path = 'image/avatar/' + avatars.filename
                    if utils.edit_player(form=request.form, avatar=avatar_path):
                        if avatars:
                            avatars.save(os.path.join(app.root_path, 'static/', avatar_path))
                        flash("Lưu thông tin cầu thủ thành công", category="success")
                        return redirect(url_for('players'))
                    else:
                        flash("Lỗi lưu thông tin cầu thủ", category="error")
            except ValueError as e:
                flash(e, category="error")
            except Exception as e:
                flash('Lỗi thêm cầu thủ', category='error')
                print("Error router creatPlayer:", e)

    params['lsplayer'] = utils.get_list_player(teamid=current_user.id)
    return render_template('user/player.html', params=params)


@app.route("/user/players/createplayer", methods=["POST", "GET"])
@decorate.login_required_user
def creatPlayer():
    params = {
        'title': 'Thêm cầu thủ',
        'nav_player': 'active',
        'positions': models.Position.query.all(),
        'genders': models.EGender,
        'tyepeplayer': models.ETyEpePlayer,
        'form': request.form
    }
    if request.method == "POST":
        try:
            if utils.check_form_add_player(teamid=current_user.id, form=request.form):
                avatars = request.files["avatar"]
                avatar_path = 'image/avatar/' + avatars.filename
                if utils.creat_player(teamid=current_user.id, form=request.form, avatar=avatar_path):
                    if avatars:
                        avatars.save(os.path.join(app.root_path, 'static/', avatar_path))
                    flash("Thêm cầu thủ thành công", category="success")
                    return redirect(url_for('creatPlayer'))
                else:
                    flash("Lỗi thêm cầu thủ", category="error")
        except ValueError as e:
            flash(e, category="error")
        except Exception as e:
            flash('Lỗi thêm cầu thủ', category='error')
            print("Error router creatPlayer:", e)

    return render_template('user/createplayer.html', params=params)



if __name__ == '__main__':
    a = models.Player.query.first().birthdate.strftime("%Y-%m-%d")

    print(a)
