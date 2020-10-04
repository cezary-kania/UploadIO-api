from Models import main_db as db
from sqlalchemy.orm import relationship
from Models.Users.StorageElModel import StorageElModel
class StorageModel(db.Model):
    
    __tablename__ = 'Storages'
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = relationship('UserModel', back_populates = 'storage')
    storage_elements = relationship('StorageElModel', back_populates = 'storage')

    def __repr__(self):
        return f'StorageModel<user_id = {self.user_id}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        self.clear()
        db.session.delete(self)
        db.session.commit()

    def get_free_space_info(self):
        pass

    def add_file(self, file):
        stElement = StorageElModel(file)
        stElement.storage = self 
        stElement.save()

    def delete_element(self, element_id):
        pass

    def clear(self):
        for el in self.storage_elements:
            el.delete()
    