from flask_wtf import FlaskForm, form
from flask import flash, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, fields, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, ValidationError
import hashlib
from webapp.models import Team,EActive
from webapp import utils, models


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validators.length(1, 50, "Nhập tối 5 đến 50 ký tự")])
    password = PasswordField('Password', validators=[DataRequired(), validators.length(8, 50)])
    remember_me = BooleanField('Remember me', default=False)


    submit = SubmitField('Sign In')

    def __init__(self, *k, **kk):
        self._user = None  # for internal user storing
        super(LoginForm, self).__init__(*k, **kk)

    def validate(self):
        #print(self.username.data)

        self._user = Team.query.filter(Team.username == self.username.data,Team.active == EActive.Active.value).first()
        #flash(self._user.password)
        return super(LoginForm, self).validate()

    def validate_username(self, field):
        if self._user is None:
            flash("Invalid username or password", category='error')
            return

    def validate_password(self, field):
        if self._user:
            if not self._user.invalid:
                if not utils.check_password_first(self._user.password,self.password.data):
                    flash("Invalid username or password", category='error')
                    self._user = None
            elif not utils.check_password(self._user.password, self.password.data):
                flash("Invalid username or password", category='error')
                self._user = None
            return

    def get_user(self):
        return self._user
class FormChangePassword(FlaskForm):
    password_Old = PasswordField('Password', validators=[DataRequired()])
    password_New = PasswordField('New Password', validators=[DataRequired()])
    password_Comfirm = PasswordField('Confirm Password ', validators=[DataRequired()])

