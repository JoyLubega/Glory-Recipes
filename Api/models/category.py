from datetime import datetime

from Api.api import db

class CategoryModel(db.Model):
    """
    Category database Model
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    __table_args__ = (db.UniqueConstraint(
        'user_id', 'name', name='unq_b_name'),)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def save(self):
        """
        Save category to data store
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        """Updates category"""
        db.session.commit()


    @staticmethod
    def get_all():
        """Get all categories"""
        CategoryModel.query.all()

    def delete(self):
        """Delete Category"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Category: {}>".format(self.name)
