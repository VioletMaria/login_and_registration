from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def reg_and_log():
    return render_template("index.html")


@app.route("/register",methods=["POST"])
def create_user():
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":pw_hash,
            "confirm_password":pw_hash
        }
        user_id = User.insert_user(data)
        session["user_id"] = user_id  # store user id into session
        flash("User created!", "register")
        return redirect("/welcome")
    else:
        return redirect("/")


@app.route("/login",methods=["POST"])
def login():
    # see if the username exists in the database
    user_in_db = User.get_by_email(request.form)
    # user is not registered
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password", "login")  # if false after checking password
        return redirect("/")
    # if passwords match, set user_id into session
    session["user_id"] = user_in_db.id
    return redirect("/welcome")


@app.route("/welcome")
def user_page():
    if "user_id" not in session:
        flash("Must be logged in!", "register")
        return redirect("/")
    else:
        data = {
            "user_id": session["user_id"]
        }
        user = User.get_user(data)
        print(user)
        return render_template("welcome.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!", "login")
    return redirect("/")
