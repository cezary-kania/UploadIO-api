from Models import main_db as db
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import date

class UserModel(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(100), unique = True, nullable = False)
    pass_hash = db.Column(db.String(256), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    account_creation_date = db.Column(db.String(10))
    
    def __init__(self, login, password, email):
        self.login = login
        self.pass_hash = sha256.hash(password)
        self.email = email
        self.account_creation_date = str(date.today())
    
    @staticmethod
    def add(user_obj):
        db.session.add(user_obj)
        db.session.commit()
    
    @staticmethod
    def get_user(**credentials):
        if 'login' in credentials.keys():
            return UserModel.query.filter_by(login = credentials['login']).first()
        if 'email' in credentials.keys():
            return UserModel.query.filter_by(email = credentials['email']).first()
        return None

    @staticmethod
    def delete_user(user_login):
        deleted = UserModel.query.filter_by(login = user_login).first().delete()
        db.session.commit()
        return deleted == 1

    @staticmethod
    def get_all_users():
        return UserModel.query.all()