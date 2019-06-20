from datetime import datetime

from Api.api import db


class ReviewsModel(db.Model):
    """
    Review Database Model includes comments and rates
    """
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    comment_text = db.Column(db.String(100))
    rate = db.Column(db.Integer, nullable=False)

    def __init__(self, comment_text, recipe_id, rate):
        self.comment_text = comment_text
        self.recipe_id = recipe_id
        self.rate = rate

    def save(self):
        """
        Save reviews  to Data Store
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all Reviews"""
        ReviewsModel.query.all()

    def delete(self):
        """Delete a reeview"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return (
            "<Comment: {}>",
            "<Rate: {}>",
            "<recipe_id: {}>".format(self.comment_text, self.rate, self.recipe_id)) # noqa E501
