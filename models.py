from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

# models


class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id = {u.id} first_name = {u.first_name} last_name = {u.last_name} test_url = {u.img_url}"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String, nullable=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # .sort() in SQL


class Post(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        return f"<Post id={self.id} title={self.title} content= {self.content} created_at={self.created_at}"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user_posts = db.relationship('User', backref='posts')
