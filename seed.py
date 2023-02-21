"""Seed file to make sample data for pets db."""

from models import User, db, Post
from app import app

# Create all tables
db.drop_all()  # drop all tables from database
db.create_all()

# If table isn't empty, empty it
User.query.delete()  # delete everything
Post.query.delete()

# Add pets
whiskey = User(first_name='Whiskey', last_name="dog", img_url="pending")
bowser = User(first_name='Bowser', last_name="dog", img_url="pending")
spike = User(first_name='Spike', last_name="porcupine", img_url="pending")

# Add posts
post1 = Post(title="hi", content="hi again", user_id=1)

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)
db.session.add(post1)

# Commit--otherwise, this never gets saved!
db.session.commit()
