from webapp import app, login, models, jinja_filters,config_main,SentEmail
from flask import request,g, render_template, redirect, url_for, abort, current_app, flash
from flask_login import current_user, login_user, logout_user, login_required, login_url, AnonymousUserMixin, \
    fresh_login_required
# from webapp.admin import *
from webapp.routerAdmin import *
from webapp.routerUser import *

config_main = models.Config.query.one()

@app.route('/')
def home():
    params = {
        'title': 'Home',
        'nav_home': 'active'
    }
    return render_template("home/index.html", params=params)


@app.route('/result')
def result():
    params = {
        'title': 'Result',
        'nav_result': 'active'
    }
    return render_template('home/result.html', params=params)


@app.route('/match')
def match():
    params = {
        'title': 'Match',
        'nav_match': 'active'
    }
    return render_template('home/match.html', params=params)


@app.route('/schedule')
def schedule():
    params = {
        'title': 'Schedule',
        'nav_schedule': 'active'
    }
    return render_template('home/schedule.html', params=params)

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


@app.route("/user/profile")
@app.route("/admin/profile")
@login_required
def profile():
    # request.args.get('id')
    # http: // 127.0.0.1: 5000 / admin / profile?id = 3f7d454b - 0283 - 4389 - a439 - b5e0b3a4c650
    """
    hiển thị thong tin chi tiết của user
    :return:
    """
    id_user = request.args.get("id")
    # print(id_blog)
    if id_user is None:
        abort(404)
    params = {
        'title': "Profile",
        'nav_user': 'active'
    }
    if current_user.role == models.Role.admin:
        params['user'] = utils.get_team_by_ID(id=id_user)
        return render_template('profile.html', params=params)

    params['user'] = current_user
    return render_template('profile.html', params=params)


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

@app.route("/admin/createround")
def create_round():
    pass



if __name__ == '__main__':
    app.run(debug=True)
