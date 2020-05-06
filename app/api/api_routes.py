import os
from app.api import blueprint
from app import db, mail
from app.models import Appuser
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from flask import jsonify, request, url_for, make_response
from functools import wraps
from flask_mail import Message
import re


def provide_token(f):
    """
    Will check if token is in headers.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'msg': 'Please provide a token, you will get one when you log in!'}), 401
        try:
            token_data = jwt.decode(token, os.environ.get('SECRET_KEY'))
            rest_api_user = Appuser.query.filter_by(
                id=token_data['id']).first()
        except:
            return jsonify({'msg': 'Token is invalid'}), 401
        return f(rest_api_user, *args, **kwargs)
    return decorated


EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
@blueprint.route('/api_routes/create_user', methods=['POST'])
def create_user():
    """
    Endpoint to create new user.
    """
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    user = Appuser.query.filter_by(email=data['email']).first()
    email = data['email']
    password = data['password']
    if user:
        return jsonify({'msg': 'User with that email allready exist in database, please use another email.'})
    elif not EMAIL_REGEX.match(email):
        return jsonify({'msg': 'Please enter a valid email address'})
    elif len(password) < 6:
        return jsonify({'msg': 'Your password must be longer than 6 characters'})
    else:
        new_user = Appuser(
            fullname=data['fullname'], email=data['email'], hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'msg': 'You are successfully create an account'}), 200


@blueprint.route('/api_routes/login')
def login():
    """
    Endpoint for login created user.
    """
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    user = Appuser.query.filter_by(email=auth.username).first()
    if not user:
        return jsonify({'msg': 'There is no user with that email'})
    if check_password_hash(user.hashed_password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=90)},
                           os.environ.get('SECRET_KEY'))
        return jsonify({'token': token.decode('utf-8')})
    return jsonify({'msg': 'Invalid password for that user!'})


@blueprint.route('/api_routes/all_users', methods=['GET'])
@provide_token
def get_all_users(rest_api_user):
    """
    This endpoint will retrive list of all users only for authenticated user,
    authenticated user will get token when sign up with correct credentials
    """
    if not rest_api_user:
        return jsonify({'msg': 'You cannot take a look on this page'})
    users = Appuser.query.all()
    all_users = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['fullname'] = user.fullname
        user_data['email'] = user.email
        all_users.append(user_data)
    return jsonify({'List of all registered users': all_users})


def send_email_to_reset_password(user):
    """
    This method will also send email to user who want to
    change password, slightly diffrent that the other one from web route format.
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f"""
If you ask for reset email from Postman or some other application for testing RESTful server, just copy endpoint and token to Postman to reset password,
also you need to provide two field in json format, password and confirm_password.
{url_for('api.reset_password', token=token)}

If you didn't ask for reset password, just ignore this email.
    """
    mail.send(msg)


@blueprint.route('/api_routes/request_reset', methods=['GET'])
def request_reset():
    """
    Enpoint for password reset request.
    """
    data = request.get_json()
    user = Appuser.query.filter_by(email=data['email']).first()
    if user:
        send_email_to_reset_password(user)
        return jsonify({'msg': 'Instructions has been sent to your email address'})
    else:
        return jsonify({'msg': 'There is no user with that email in our database.'})


@blueprint.route('/api_routes/reset_password/<token>', methods=['POST'])
def reset_password(token):
    """
    Endpoint for password reset.
    """
    user = Appuser.verify_reset_token(token)
    if user is None:
        return jsonify({'msg': 'Your token is invalid or expired!!!'})
    data = request.get_json()
    if data['password'] != data['confirm_password']:
        return jsonify({'msg': 'Your password must match with confirm password field !!!'})
    else:
        user.set_password(data['password'])
        db.session.commit()
        return jsonify({'msg': 'Your are successfully create new password, now you can login with new password.'})
