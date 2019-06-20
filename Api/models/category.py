from datetime import datetime

from Api.api import db


class CategoryModel(db.Model):
    """
    Category database Model
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False,)
    parent_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=True)
    children = db.relationship("CategoryModel")

    def __init__(self, name, created_by, parent_id):
        self.name = name
        self.created_by = created_by
        self.parent_id = parent_id

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
