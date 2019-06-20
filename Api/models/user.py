from Api.api import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    """
    User Database model
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    status = db.Column(db.String(100))

    def __init__(self, email, password, name=None):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)

    @staticmethod
    def check_password(pw_hash, password):
        """
        Validates password
        :param pw_hash:
        :param password:
        """
        return check_password_hash(pw_hash, password)

    def save(self):
        """
        Save User to Data store
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        """Updates user"""
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all Users"""
        return UserModel.query.all()

    def delete(self):
        """Delete User"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<User: {}>".format(self.name)
