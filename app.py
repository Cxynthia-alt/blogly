from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    return render_template("add_new_post.html", user=user)


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
    return render_template("user_post.html", post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_page(post_id):
    post = Post.query.get(post_id)
    return render_template("edit_post.html", post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_current_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form["post_title"]
    post.content = request.form["post_content"]
    db.session.add(post)
    db.session.commit()
    return redirect("/")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_current_post(post_id):
    Post.query.filter(id=post_id).delete()
    db.session.commit()
    return redirect("/")
