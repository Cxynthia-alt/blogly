"""Seed file to make sample data for pets db."""

from models import User, db, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()  # drop all tables from database
db.create_all()

# If table isn't empty, empty it
User.query.delete()  # delete everything
Post.query.delete()
Tag.query.delete()


# Add pets
whiskey = User(first_name='Whiskey', last_name="dog", img_url="pending")
bowser = User(first_name='Bowser', last_name="dog", img_url="pending")
spike = User(first_name='Spike', last_name="porcupine", img_url="pending")

# Add posts
post1 = Post(title="hi", content="hi again", user_id=1)
post2 = Post(title="how are you", content="All good", user_id=1)
post3 = Post(title="Goodbye", content="Bye!", user_id=2)
post4 = Post(title="Small Talk", content="What do you do for fun", user_id=3)


# Add tags
tag1 = Tag(name='greeting')
tag2 = Tag(name='farewell')
tag3 = Tag(name='chat')

# Add post_tags
post_tag1 = PostTag(post_id=1, tag_id=1)
post_tag2 = PostTag(post_id=2, tag_id=1)
post_tag3 = PostTag(post_id=3, tag_id=1)
post_tag4 = PostTag(post_id=4, tag_id=3)


# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(post_tag1)
db.session.add(post_tag2)
db.session.add(post_tag3)
db.session.add(post_tag4)


# Commit--otherwise, this never gets saved!
db.session.commit()
