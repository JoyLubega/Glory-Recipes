from datetime import datetime

from Api.api import db

class CommentsModel(db.Model):
    """
    Comments Database Model
    """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    comment_text = db.Column(db.String(100))
    

    def __init__(self, comment_text, recipe_id):
        self.comment_text = comment_text
        self.recipe_id = recipe_id

    def save(self):
        """
        Save Comments  to Data Store
        """
        db.session.add(self )
        db.session.commit()


    @staticmethod
    def get_all():
        """Get all Items"""
        CommentsModel.query.all()

    def delete(self):
        """Delete Item"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Comment: {}>".format(self.comment_text)