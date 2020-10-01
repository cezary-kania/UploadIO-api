from . import main_db as db, gfs
from sqlalchemy.orm import relationship
from bson import ObjectId
from Models.UploadModel import UploadModel

class UploadedFileModel(db.Model):
    __tablename__ = 'UploadedFiles'
    
    id = db.Column(db.Integer, primary_key = True)
    upload_id = db.Column(db.Integer, db.ForeignKey('Uploads.id'))
    number_in_upload = db.Column(db.Integer, nullable = False)
    upload = relationship("UploadModel", back_populates='uploaded_files')
    filename = db.Column(db.String(300), nullable = False)
    mongo_id = db.Column(db.String(20), nullable = False)
    
    def __init__(self, upload_id,number_in_upload, file):
        self.filename = file.filename
        self.number_in_upload = number_in_upload
        self.upload_id = upload_id
        self.mongo_id = str(gfs.put(file, content_type = file.content_type, filename = file.filename))

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'UploadedFileModel<{self.upload_id},{self.number_in_upload}, {self.filename}>'

    @staticmethod
    def get_file_by_upload(url_hash,password, file_index):
        result_upload = UploadModel.query.filter_by(url_hash = url_hash).first()
        if result_upload is None:
            raise Exception("Upload not found.")
        if not result_upload.verify_pass(password):
            raise Exception("Password incorrect.")
        result_file = UploadedFileModel.query.filter_by(upload_id = result_upload.id, number_in_upload = file_index).first()
        if result_file is None:
            raise Exception("File not found.")
        file = gfs.get(ObjectId(result_file.mongo_id))
        return file