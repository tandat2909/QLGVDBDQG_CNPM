from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect

from webapp import db, admin, models


class LogoutView(BaseView):
    @expose('/logout')
    def index(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated
class AuthenticationView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated



admin.add_view(AuthenticationView(models.User, db.session))
admin.add_view(AuthenticationView(models.Round,db.session))
admin.add_view(AuthenticationView(models.Result,db.session))
admin.add_view(AuthenticationView(models.Player,db.session))
admin.add_view(AuthenticationView(models.Team,db.session))
admin.add_view(AuthenticationView(models.Match,db.session))