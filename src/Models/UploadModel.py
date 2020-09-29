from . import db
from sqlalchemy.orm import relationship
class UploadModel(db.Model):
    
    __tablename__ = 'uploads'
    
    id = db.Column(db.Integer, primary_key = True)
    url_hash = db.Column(db.String(10), nullable = False)
    password = db.Column(db.String(100))
    expiration_date = db.Column(db.String(20))

    def __init__(self, upload_pass = None, expiration_date = None):
        self.url_hash = UploadModel.get_new_url_hash()
        self.password = upload_pass
        self.expiration_date = expiration_date

    def save(self):
        db.session.add(self)
        db.session.commit()
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
        

