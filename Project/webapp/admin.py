from flask_admin import BaseView, expose,form
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView
from flask_admin.model.template import LinkRowAction
from flask_login import logout_user, current_user
from flask import redirect,url_for

from wtforms import validators, PasswordField, HiddenField, StringField, Field, widgets,RadioField
from wtforms.fields.html5 import EmailField,TelField

from webapp import db, admin, models


class LogoutView(BaseView):
    @expose('/logout')
    def index(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated
class AuthenticationView(ModelView,BaseView):
    def is_accessible(self):
        return True

class UserView(AuthenticationView):
    form_base_class = form.SecureForm
    edit_modal = True
    action_disallowed_list = ['delete']
    can_delete = False
    details_modal = True
    list_template = 'list.html'

    column_filters = ('name','username','email','phonenumber')
    column_searchable_list = column_filters

    column_list = (
        'username',
        'name',
        'email',
        'phonenumber',
        'role',
        'active',
        'match'

    )



    form_columns = (
        'username',
        'password',
        'name',
        'email',
        'phonenumber',
        'active'
    )
    form_edit_rules ={
        'username',
        'name',
        'email',
        'phonenumber',
        'active'
    }
    column_editable_list = (
        #'name',
        #'phonenumber',
        #'username',
        #'role',
        'active',
        #'email'
    )

    form_extra_fields = {
        'password': PasswordField("Password",
                                  validators=[validators.data_required(), validators.length(min=8, max=100)]),
        'email': EmailField("Email", validators=[validators.data_required()]),
        'name': StringField("Full Name", validators=[validators.data_required()]),
        'phonenumber':TelField("Phone Number"),
        #'active': RadioField("Active")
    }




admin.add_view(UserView(models.User, db.session))
admin.add_view(AuthenticationView(models.Round,db.session))
admin.add_view(AuthenticationView(models.Result,db.session))
admin.add_view(AuthenticationView(models.Player,db.session))
admin.add_view(AuthenticationView(models.Team,db.session))
admin.add_view(AuthenticationView(models.Match,db.session))