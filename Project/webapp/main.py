from sqlalchemy.sql.functions import user

from webapp import app, login, models, jinja_filters, SentEmail
from flask import request, g, render_template, redirect, url_for, abort, current_app, flash
from flask_login import current_user, login_user, logout_user, login_required, login_url, AnonymousUserMixin, \
    fresh_login_required
# from webapp.admin import *
from webapp.routerAdmin import *
from webapp.routerUser import *


@app.route('/')
def home():
    params = {
        'title': 'Home',
        'nav_home': 'active',
    }
    params['results'] = models.Result.query.all()
    params['teams'] = models.Team
    params['groups'] = models.Groups.query.all()
    return render_template("home/index.html", params=params)


@app.route('/search')
def find():
    kw = request.args.get("kw")
    players = utils.find_player_by_name(kw)
    teams = utils.find_team_by_name(kw)
    print(kw, players, teams)
    params = {
        'title': 'Home',
        'nav_home': 'active',
        'players': players,
        'teams': teams,
        'groups': models.Groups.query.all()
    }
    return render_template("home/search.html", params=params)


@app.route('/result')
def result():
    params = {
        'title': 'Result',
        'nav_result': 'active'
    }
    params['results'] = models.Result.query.all()
    params['teams'] = models.Team
    params['groups'] = models.Groups.query.all()
    return render_template('home/result.html', params=params)


@app.route('/schedule')
def schedule():
    params = {
        'title': 'Schedule',
        'nav_schedule': 'active'
    }
    params['results'] = models.Result
    params['matchs'] = models.Match.query.all()
    params['teams'] = models.Team
    params['groups'] = models.Groups.query.all()
    return render_template('home/schedule.html', params=params)


@app.route("/player/profile")
def player_profile():
    params = {
        'title': 'Playerprofile',
    }
    params['player'] = utils.get_player_by_ID(request.args.get('idp'))

    return render_template('home/playerprofile.html', params=params)


@app.route("/team/profile")
def team_profile():
    params = {
        'title': 'teamprofile',
    }
    params['team'] = utils.get_team_by_ID(request.args.get('idp'))
    params['players'] = models.Team.query.get(request.args.get('idp')).players
    params['groups'] = models.Groups.query.all()


    return render_template('home/teamproflie.html', params=params)


@app.route("/register", methods=['GET', 'POST'])
def register():
    pass


@app.route('/changepw', methods=["POST", "GET"])
@fresh_login_required
def change_password():
    """
    thay đổi password

    :return:
    """
    params = {
        'title': "Change password",
        'nav_user': 'active',

    }
    form = Forms.FormChangePassword()
    params['form'] = form
    if form.validate_on_submit():
        pwold = form.password_Old.data
        pwnew = form.password_New.data
        pwconf = form.password_Comfirm.data

        if current_user.is_authenticated:
            if len(pwold) >= 8 and utils.check_password(current_user.password, pwold):
                if [len(pwnew), len(pwconf)] >= [8, 8]:
                    if utils.change_password(user=current_user, pwold=pwold, pwnew=pwnew):
                        flash('Change password success')
                        return redirect(
                            url_for('login_admin' if current_user.role == models.Role.admin else 'login_us'))
                    else:
                        flash("Change password error")

                else:
                    flash("Nhập password trên 8 ký tự")
            else:
                flash('Password old incorrect')
        else:
            abort(404)
    return render_template('ChangePassword.html', params=params)


@app.route('/user/changepwfirst', methods=['POST', 'GET'])
@decorate.login_first
def changepwfirst():
    form = Forms.FormChangePassword()
    if form.validate_on_submit():
        pwold = form.password_Old.data
        pwnew = form.password_New.data
        pwconf = form.password_Comfirm.data
        if pwnew == pwconf:
            if len(pwold) >= 8 and utils.check_password_first(current_user.password, pwold):
                if [len(pwnew), len(pwconf)] >= [8, 8]:
                    if utils.change_password(user=current_user, pwold=pwold, pwnew=pwnew):
                        flash('Đổi mật khẩu thành công', category='success')
                        return redirect(url_for('index_user'))
                    else:
                        flash("lỗi thay đổi mật khẩu", category='error')
                else:
                    flash("Nhập mật khẩu trên 8 ký tự", category='error')
            else:
                flash('Mật khẩu không đúng ', category='error')
        else:
            flash("Mật khẩu xác nhận sai", category='error')
    return render_template('changepwfirst.html', form=form, title="Change password first")


@app.route("/user/profile-player")
@app.route("/admin/profile-player")
@login_required
def profile_player():
    """
    hiển thị thong tin chi tiết của player
    :return:
    """
    playerid = request.args.get("idp")
    player = utils.get_player_by_ID(playerid)
    if player is None:
        abort(404)
    params = {
        'title': "Thông tin cầu thủ",
        'player': player
    }
    return render_template('profile.html', params=params)


@app.route("/user/profile-team", methods=['POST', 'GET'])
@app.route("/admin/profile-team")
@login_required
def profile_team():
    teamid = request.args.get("idt")
    team = utils.get_team_by_ID(teamid)
    if request.method == "POST":
        try:
            email = request.form.get('email')
            phone = request.form.get('phonenumber')
            stadium = request.form.get('stadium')
            logo= request.files["logo"]
            logo_path = 'image/logoTeam/' + logo.filename

            if utils.change_team_profile(email=email, phone=phone, stadium=stadium,logo = logo_path, idteam=current_user.id):
                logo.save(os.path.join(app.root_path, 'static/', logo_path))
                flash("Thay đổi thông tin đội bóng thành công!", category="success")
            else:
                flash("Thay không thành công!", category="success")
            return redirect(url_for('profile_team', idt=current_user.id))
        except ValueError as e:
            flash(e,category="error")
            return redirect(url_for('profile_team', idt=current_user.id))
        except Exception as e:
            print('lỗi profile_team', e)
            return redirect(url_for('profile_team', idt=current_user.id))
    if team is None:
        abort(404)
    params = {
        'title': "Thông tin đội bóng",
        'team': team
    }

    return render_template('profile_team.html', params=params)


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/admin')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', code=404, ms='Error Page'), 404


@app.errorhandler(405)
def page_not_found(error):
    return render_template('error.html', code=405, ms='Error Page'), 405


@app.errorhandler(500)
def special_exception_handler(error):
    return render_template('error.html', code=500, ms='Error Page'.capitalize()), 500


@login.user_loader
def get_user(id):
    return models.Team.query.get(id)


if __name__ == '__main__':
    app.run(debug=True)
