from werkzeug.security import generate_password_hash, check_password_hash
from App.extensions import db
from datetime import datetime
from App.models.commonbaseclass import Base
from flask_login import UserMixin
from App.models.movie import Movie

class User(UserMixin,Base,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(12),index=True,nullable=False,unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50),unique=True)
    icon = db.Column(db.String(70),default='default.jpg')
    lastLogin = db.Column(db.DateTime)
    registerTime = db.Column(db.DateTime,default=datetime.utcnow)
    confirm = db.Column(db.Boolean,default=True)

    favorites = db.relationship('Movie',secondary='collections',backref=db.backref('users',lazy='dynamic'),lazy='dynamic')

    @property
    def password(self):
        raise AttributeError

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def is_favorite(self,pid):
        favorites = self.favorites.all()
        for i in favorites:
            if i.id == pid:
                return True
        return False

    def add_favorite(self,pid):
        self.favorites.append(Movie.query.get(pid))
        db.session.commit()

    def remove_favorite(self,pid):
        self.favorites.remove(Movie.query.get(pid))
        db.session.commit()

    def __str__(self):
        return self.username


from App.extensions import login_manager
@login_manager.user_loader
def user_loader(userid):
    return User.query.get(int(userid))