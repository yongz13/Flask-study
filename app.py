from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = "something-secret"  # use a better secret in production

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    name = ""
    if request.method == "POST":
        name = request.form.get("username")
    return render_template("index.html", name=name)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/greet", methods=["GET", "POST"])
def greet():
    if request.method == "POST":
        friend_name = request.form.get("friendname")
        session["friend_name"] = friend_name
        return redirect(url_for("greeted", name=friend_name))
    return render_template("greet.html")

@app.route("/greeted")
def greeted():
    name = session.get("friend_name", "")
    return render_template("greeted.html", name=name)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("greet"))

@app.route("/guestbook", methods=["GET", "POST"])
def guestbook():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")

        if name and message:
            new_entry = Entry(name=name, message=message)
            db.session.add(new_entry)
            db.session.commit()

        return redirect(url_for("guestbook"))

    all_entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template("guestbook.html", entries=all_entries)


@app.route("/guestbook/clear")
def clear_guestbook():
    db.session.query(Entry).delete()
    db.session.commit()
    return redirect(url_for("guestbook"))


