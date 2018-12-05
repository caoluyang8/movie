from App.extensions import db
from .commonbaseclass import Base

class Movie(Base,db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer,primary_key=True)
    moviename = db.Column(db.String(20))
    moviesynopsis = db.Column(db.Text) #电影简介
    collection = db.Column(db.Integer,default=0)
    movielength = db.Column(db.Integer,default=0)
    movieicon = db.Column(db.String(70), default='default2.jpg')

    def __str__(self):
        return self.moviename