from Models import main_db as db, gfs
from sqlalchemy.orm import relationship
from bson import ObjectId

from Models.Uploads.UploadModel import UploadModel
from Models.Uploads.UploadedFileModel import UploadedFileModel

class StorageElModel(db.Model):
    
    __tablename__ = 'StorageElements'
    
    id = db.Column(db.Integer, primary_key = True)
    storage_id = db.Column(db.Integer, db.ForeignKey('Storages.id'))
    storage = relationship('StorageModel', back_populates = 'storage_elements')
    el_type = db.Column(db.String(20), nullable = False)
    filename = db.Column(db.String(300), nullable = False)
    mongo_id = db.Column(db.String(20), nullable = False)
    is_shared = db.Column(db.Boolean, nullable = False, default = False)
    share_url = db.Column(db.String(10), default = None)

    def __init__(self, file, el_type = 'file'):
        self.filename = file.filename
        self.el_type = el_type 
        self.mongo_id = str(gfs.put(file, content_type = file.content_type, filename = file.filename))

    def __repr__(self):
        return f'StorageElModel<filename = {self.filename}, mongo_id = {self.mongo_id}, is_shared = {self.is_shared}, >'
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        gfs.delete(ObjectId(self.mongo_id))
        db.session.delete(self)
        db.session.commit()
    
    def get_file(self):
        return gfs.get(ObjectId(self.mongo_id))

    def share(self, upload_pass = None):
        upload = UploadModel(upload_pass)
        uploaded_file = UploadedFileModel(
            {"filename" : self.filename, "mongo_id" : self.mongo_id},
            user_upload = True
        )
        uploaded_file.upload = upload 
        upload.save()
        self.is_shared = True
        self.share_url = upload.url_hash 
    def disable_sharing(self):
        self.is_shared = True
        upload = UploadModel.get_upload_by_url_hash(self.share_url)
        upload.is_active = False
    def get_share_info(self):
        return {
            "is_shared" : self.is_shared,
            "share_url" : self.share_url
        }