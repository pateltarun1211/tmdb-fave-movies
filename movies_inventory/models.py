from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import uuid
from werkzeug.security import generate_password_hash
import secrets
from datetime import datetime
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default ='')
    last_name = db.Column(db.String(150), nullable = True, default ='')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True)
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    movie = db.relationship('SaveMovie', backref = 'owner', lazy=True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash


    def __repr__(self):
        return f"User {self.email} has been added to the database!"

class Movie:
    """
    Movie class to define Movie Objects
    """

    def __init__(self,id,title,overview,poster):
        self.id = id
        self.title = title
        self.overview = overview
        self.poster = f"https://image.tmdb.org/t/p/w500/{poster}"

class SaveMovie(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(100))
    tmdb_id = db.Column(db.String)
    overview = db.Column(db.String)
    poster = db.Column(db.String)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    
    def __init__(self, title, tmdb_id, overview, poster, user_token, id = ''):
        self.id = self.set_id()
        self.title = title
        self.tmdb_id = tmdb_id
        self.overview = overview
        self.poster = poster
        self.user_token = user_token
    
    def __repr__(self):
        return f"The following Movie has been added: {self.name}"
    
    def set_id(self):
        return secrets.token_urlsafe()
    
    
class SaveMovieSchema(ma.Schema):
    class Meta:
        fields = ['id', "title", "tmdb_id", 'overview', 'poster']

movie_schema = SaveMovieSchema()
movies_schema = SaveMovieSchema(many = True)

