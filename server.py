from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=["GET"])
def register_form():

    email_input = request.form['email']
    password_input = request.form['password']


    if User.query.filter_by(email=email_input).one():
        redirect("/user_list")
    else:
        new_user = User(email=email_input,password=password_input)
        db.session.add(new_user)
        db.session.commit()
    

    # if password == 'let-me-in':   # FIXME # get password from database if it exists
    #     session['current_user'] = username
    #     flash("Logged in as %s" % username)
    #     return redirect("/")

    # else:
    #     flash("Wrong password!")
    #     return redirect("/login")

    person = request.args.get('email')


    return render_template("register_form.html") 



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
