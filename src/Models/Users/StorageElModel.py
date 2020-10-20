from Models import main_db as db, gfs
from sqlalchemy.orm import relationship
from bson import ObjectId
import re

from Models.Uploads.UploadModel import UploadModel
from Models.Uploads.UploadedFileModel import UploadedFileModel
from Utils.file_operators import get_file_size
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
    size = db.Column(db.Integer, nullable = False)
    
    def __init__(self, file, storage_id, el_type = 'file'):
        self.set_filename(file.filename, storage_id)
        self.el_type = el_type 
        self.mongo_id = str(gfs.put(file, content_type = file.content_type, filename = file.filename))
        self.size = get_file_size(file)
    def __repr__(self):
        return f'StorageElModel<filename = {self.filename}, mongo_id = {self.mongo_id}, is_shared = {self.is_shared}, >'
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    def save(self):
        db.session.commit()
    def delete(self):
        if self.is_shared is True:
            self.disable_sharing()
        gfs.delete(ObjectId(self.mongo_id))
        db.session.delete(self)
        db.session.commit()
    
    def get_file(self):
        return gfs.get(ObjectId(self.mongo_id))
    
    def set_filename(self, new_filename, storage_id):
        existing_file = StorageElModel.query.filter_by(filename = new_filename, storage_id = storage_id).first()
        while existing_file is not None:
            new_filename = StorageElModel.generate_new_filename(new_filename)
            existing_file = StorageElModel.query.filter_by(filename = new_filename, storage_id = storage_id).first()
        self.filename = new_filename
    
    def share(self, upload_pass = None):
        upload = UploadModel(upload_pass)
        uploaded_file = UploadedFileModel(
            {"filename" : self.filename, "mongo_id" : self.mongo_id},
            user_upload = True
        )
        upload.size = self.size
        uploaded_file.upload = upload 
        upload.save()
        self.is_shared = True
        self.share_url = upload.url_hash 

    def disable_sharing(self):
        self.is_shared = False
        upload = UploadModel.get_upload_by_url_hash(self.share_url)
        self.share_url = None
        upload.is_active = False
        db.session.commit()
    def get_share_info(self):
        return {
            "is_shared" : self.is_shared,
            "share_url" : self.share_url
        }
    @staticmethod
    def get_element(**params):
        if 'id' in params.keys():
            return StorageElModel.query.filter_by(id = params['id']).first()
        if 'share_url' in params.keys():
            return StorageElModel.query.filter_by(share_url = params['share_url']).first()
        return None
    @staticmethod
    def get_file_size(file):
        from os import SEEK_END
        file.seek(0, SEEK_END)
        return file.tell()
    
    @staticmethod
    def generate_new_filename(filename):
        filename_parts = filename.split('.')
        ext = ''
        index = 1
        if len(filename_parts) > 1:
            ext = filename_parts[-1]
        filename = filename_parts[0]
        result = re.search('\([0-9]+\)$', filename)
        if result is not None:
          result = result.group()
          result_len = len(result)
          index = int(result[1:-1])
          index += 1
          filename = filename[:-result_len]
        if ext != '':
          filename = f'{filename}({index}).{ext}'
        else:
          filename = f'{filename}({index})'
        return filename
