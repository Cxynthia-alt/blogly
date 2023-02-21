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


@app.route('/')
def home_page():
    """Show list of all pets in db"""
    users = User.query.all()

    return render_template("list.html", users=users)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


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
