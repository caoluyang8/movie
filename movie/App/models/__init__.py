from .user import User
from .movie import Movie
from App.extensions import db


collections = db.Table('collections',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('movie_id',db.Integer,db.ForeignKey('movie.id')),
)