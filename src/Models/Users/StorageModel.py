from Models import main_db as db
from sqlalchemy.orm import relationship
from Models.Users.StorageElModel import StorageElModel
class StorageModel(db.Model):
    
    __tablename__ = 'Storages'
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = relationship('UserModel', back_populates = 'storage')
    storage_elements = relationship('StorageElModel', back_populates = 'storage')
    
    @property
    def used_space(self):
        used_space = 0
        for el in self.storage_elements:
            used_space += el.size 
        return used_space
    
    def __repr__(self):
        return f'StorageModel<user_id = {self.user_id}, used_space = {self.used_space}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        self.clear()
        db.session.delete(self)
        db.session.commit()

    def add_file(self, file):
        stElement = StorageElModel(file)
        stElement.storage = self 
        stElement.add()
        return stElement

    def delete_element(self, **args):
        if 'element_id' in args.keys():
            stElement = StorageElModel.get_element(id = int(args["element_id"]))
            stElement.delete() 
            db.session.commit()
        if 'st_element' in args.keys():
            stElement = args['st_element']
            stElement.delete()
            db.session.commit()

    def clear(self):
        for el in self.storage_elements:
            el.delete()

