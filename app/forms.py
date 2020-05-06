from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from flask_login import current_user
from app.models import Appuser


class RegistrationForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired()])
    email = StringField('Email', validators=[Length(min=6),
                                             Email(
                                                 message='Enter a valid email address.'),
                                             DataRequired()])
    password = PasswordField('Password',
                                    validators=[DataRequired(),
                                                Length(min=6, message='Select a stronger password.')])
    confirm_password = PasswordField('Repeat Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Password must match.')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Appuser.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(message='Enter a valid email address.')])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Appuser.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    hashed_password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('hashed_password')])
    submit = SubmitField('Reset Password')
