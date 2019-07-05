from datetime import datetime

from Api.api import db


class RecipeModel(db.Model):
    """
    Recipe Database Model
    """
    __tablename__ = 'recipes'
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_text = db.Column(db.String(100), index=True)
    __table_args__ = (db.UniqueConstraint(
        'category_id', 'name', name='unq_i_name'),)

    def __init__(self, name, category_id, user_id, recipe_text):
        self.name = name
        self.category_id = category_id
        self.user_id = user_id
        self.recipe_text = recipe_text

    def save(self):
        """
        Save Recipe  to Data Store
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all recipes"""
        RecipeModel.query.all()

    def delete(self):
        """Delete Item"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        """Update recipes """
        db.session.commit()

    def __repr__(self) -> str:
        return "<Recipe: {}>".format(self.name)
