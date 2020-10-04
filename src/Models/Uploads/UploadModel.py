from Models import main_db as db
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime, date as dt, timedelta 
class UploadModel(db.Model):
    
    __tablename__ = 'Uploads'
    
    id = db.Column(db.Integer, primary_key = True)
    url_hash = db.Column(db.String(10), nullable = False)
    password = db.Column(db.String(256))
    has_expired = db.Column(db.Boolean, server_default = 'f', default = False)
    expiration_date = db.Column(db.String(10))
    uploaded_files = relationship('UploadedFileModel', back_populates='upload')
    is_active = db.Column(db.Boolean)
    def __init__(self, upload_pass = None, days_to_expire = None):
        self.url_hash = UploadModel.get_new_url_hash()
        self.password = sha256.hash(upload_pass) if (upload_pass is not None) and (upload_pass is not '') else None
        self.is_active = True
        if days_to_expire is not None:
            date = dt.today()
            date += timedelta(days = days_to_expire)
            self.expiration_date = str(date) 
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def verify_pass(self, pass_to_verify):
        if self.password is None: return True
        return sha256.verify(pass_to_verify, self.password)
    
    def check_expiration_time(self):
        date = str(dt.today())
        if self.expiration_date is None: return True
        expired = self.expiration_date >= date
        self.is_active = expired
        return expired 
    def check_is_active(self):
        return self.is_active
    def is_pass_required(self):
        return self.password is not None

    @staticmethod
    def generate_url_hash():
        import string, random
        chars  = string.ascii_letters + string.digits
        hash = ''.join(random.choices(chars,k=10))
        return hash  
    
    @staticmethod
    def is_hash_used(hash):
        query = UploadModel.query.filter_by(url_hash = hash).first()
        return bool(query)

    @staticmethod
    def get_new_url_hash():
        new_hash = UploadModel.generate_url_hash()
        while UploadModel.is_hash_used(new_hash):
            new_hash = UploadModel.generate_url_hash()
        return new_hash
    
    @staticmethod    
    def get_all_uploads():
        return UploadModel.query.all()

    @staticmethod
    def get_upload_by_url_hash(url_hash):
        return UploadModel.query.filter_by(url_hash = url_hash).first()
        
