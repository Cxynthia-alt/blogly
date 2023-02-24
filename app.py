from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SECRET_KEY'] = "SECRET!"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route('/')
def home_page():
    """Show list of all pets in db"""
    users = User.query.all()

    return render_template("list.html", users=users)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter(
        Post.user_id == user_id).all()
    return render_template("details.html", user=user, user_posts=user_posts)


@app.route('/users/new')
def show_add_new_user_form():
    return render_template("create.html")


@app.route('/users/new', methods=["POST"])
def add_new_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]
    new_user = User(first_name=first_name,
                    last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/users/{new_user.id}")


@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    user = User.query.get(user_id)
    return render_template("edit.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_current_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"]
    db.session.add(user)
    db.session.commit()
    return redirect("/")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_current_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/")


# Part 2

@app.route('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    tag_names = [tag.name for tag in tags]
    return render_template("add_new_post.html", user=user, tag_names=tag_names)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_new_post(user_id):
    title = request.form["post_title"]
    content = request.form["post_content"]
    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_user_post(post_id):
    post = Post.query.get(post_id)
    user = User.query.get_or_404(post.user_id)
    post_tags = PostTag.query.filter_by(post_id=post_id).all()
    tag_ids = [post_tag.tag_id for post_tag in post_tags]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    tag_names = [tag.name for tag in tags]
    # how to get all the tag id from the post_id?
    # tags is query set: a container contains all the query results/instances
    # use all() to convert it to a python list
    return render_template("user_post.html", post=post, user=user, tag_names=tag_names)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_page(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_current_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form["post_title"]
    post.content = request.form["post_content"]
    db.session.add(post)
    db.session.commit()
    return redirect("/")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_current_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect("/")

# Part 3


@app.route('/tags')
def show_all_tags():
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tagged_posts.html", tag=tag, posts=posts)


@app.route('/tags/new')
def add_a_new_tag_form():
    return render_template("add_tag.html")


@app.route('/tags/new', methods=["POST"])
def submit_a_new_tag():
    tag_name = request.form["tag_name"]
    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")


@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def submit_edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["tag_name"]
    db.session.add(tag)
    db.sessiion.commit()
    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_current_tag(tag_id):
    Tag.query.filter_by(id=tag_id).delete()
    db.sessiion.commit()
    return redirect("/tags")
