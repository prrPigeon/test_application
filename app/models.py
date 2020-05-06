import os
from app import app, db, login
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for, jsonify
import base64
from datetime import datetime, timedelta


@login.user_loader
def load_user(user_id):
    return Appuser.query.get(int(user_id))


class Appuser(UserMixin, db.Model):
    """
    fullname is not unique, assuming that
    there is more than one person with 
    same name.
    """
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    hashed_password = db.Column(db.String(120))

    def get_reset_token(self, expires_sec=1800):
        """
        token will last 30 minutes.
        """
        s = Serializer(os.environ.get('SECRET_KEY'), expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        With this staticmetod we tell python to not 
        expect self as argument, just token.
        """
        s = Serializer(os.environ.get('SECRET_KEY'))
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Appuser.query.get(user_id)

    def __repr__(self):
        return f"{self.fullname}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
