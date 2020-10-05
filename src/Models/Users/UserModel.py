from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import date

from Models import main_db as db

from .StorageElModel import StorageElModel
from .StorageModel import StorageModel

class UserModel(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(100), unique = True, nullable = False)
    pass_hash = db.Column(db.String(256), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    account_creation_date = db.Column(db.String(10))
    account_type = db.Column(db.String(20), default = 'user', nullable = False)
    storage = relationship('StorageModel',uselist=False, back_populates='user')

    def __init__(self, login, password, email):
        self.login = login
        self.pass_hash = sha256.hash(password)
        self.email = email
        self.account_creation_date = str(date.today())
        self.storage = StorageModel()
        self.storage.user = self
        self.storage.save()

    def validate_pass(self, pass_to_validate):
        return sha256.verify(pass_to_validate, self.pass_hash)
    
    def change_pass(self, new_pass):
        self.pass_hash = sha256.hash(new_pass)
        db.session.commit()
    
    def set_type(self, account_type):
        self.account_type = account_type if account_type in ['user', 'admin'] else 'user'
        db.session.commit()
    
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
        user = UserModel.query.filter_by(login = user_login).first()
        if user is not None:
            user.storage.delete()
            db.session.delete(user)
            db.session.commit()
            return True
        return False 

    @staticmethod
    def get_all_users():
        return UserModel.query.all()
    
    @staticmethod
    def delete_all_users():
        users = UserModel.get_all_users()
        deleted_rows = 0
        for user in users:
            UserModel.delete_user(login = user.login)
            deleted_rows += 1
        db.session.commit()
        return deleted_rows
    
    
