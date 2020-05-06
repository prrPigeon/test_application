import os
from flask import (
    render_template, redirect, url_for, request, flash
)
from app import app, db, mail
from app.forms import (
    RegistrationForm, LoginForm,
    RequestResetForm, ResetPasswordForm
)
from app.models import Appuser
from flask_login import (
    current_user, login_user, logout_user, login_required
)
from flask_mail import Message


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    fun = 'https://9gag.com/'
    return render_template('home.html', title='Home', fun=fun)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for user registering.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Appuser(fullname=form.fullname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are successfully register your account, to procced please log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Appuser.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Check your credentials please', 'warning')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash(f'Welcome {current_user}', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


def send_email_to_reset_password(user):
    """
    This method is for sending email to user
    which need to change password.
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f"""
To reset password, visit following link:
{url_for('reset_token', token=token, _external=True)}
If you didn't ask for reset password, just ignore this email.
    """
    mail.send(msg)


@app.route('/password_reset', methods=['GET', 'POST'])
def reset_request():
    """
    Route for requesting password reset.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Appuser.query.filter_by(email=form.email.data).first()
        send_email_to_reset_password(user)
        flash('Email with instruction has been sent to your email address', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Request Password Reset', form=form)


@app.route('/password_reset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """
    Route for changing user password.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Appuser.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.hashed_password.data)
        db.session.commit()
        flash('Your password has been successfully changed, to proceed please log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
