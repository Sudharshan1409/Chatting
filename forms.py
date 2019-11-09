from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from models import User,update_users

class LoginForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    phno = StringField('Phone Number',validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired()])
    submit = SubmitField('Login')

class MessageForm(FlaskForm):
    message = StringField('Message')
    submit = SubmitField('Send')

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    name = StringField('Name',validators = [DataRequired()])
    phno = StringField('Phone Number',validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired(),EqualTo('pass_confirm',message = "Password Don't Match")])
    pass_confirm = PasswordField('Confirm Password',validators = [DataRequired()])
    submit = SubmitField('Register')

    def check_email(self,field):
        if User.query.filter_by(email = field.data).first():
            return True

    def check_phno(self,field):
        if User.query.filter_by(phno = field.data).first():
            return True

class UsersButtonForm(FlaskForm):
    button = SelectField('Users',choices=update_users())
    submit = SubmitField('Submit')
