from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

app = Flask(__name__)
app.secret_key = "ilovereesiebooboo"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def main():

    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("text")
        location = request.form.get("location")
        type = request.form.get("type")

        if not title or not body or not location or not type:
            flash("Fill all boxes")
            return render_template("main.html")

        db.execute("INSERT INTO posts (user_id, type, title, body, location) VALUES(?, ?, ?, ?, ?)", session["user_id"], type, title, body, location)

        return redirect("/")


    else:
        posts = db.execute("""SELECT posts.*, users.username, users.emoji FROM posts
                           JOIN users ON posts.user_id = users.id
                           ORDER BY posts.created_at DESC""")
        for post in posts:
            post["comments"] = db.execute("""SELECT comments.*, users.username, users.emoji
                                        FROM comments
                                        JOIN users ON comments.user_id = users.id
                                        WHERE comments.post_id = ?
                                        ORDER BY comments.created_at ASC""", post["id"])


    return render_template("main.html", posts=posts)

@app.route("/comment", methods=["POST"])
@login_required
def comment():
    post_id = request.form.get("post_id")
    body = request.form.get("comment")

    if not body:
        flash("Comment can't be empty")
        return redirect("/")

    db.execute("INSERT INTO comments (post_id, user_id, body) VALUES(?, ?, ?)",
               post_id, session["user_id"], body)

    return redirect("/")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    return render_template("settings.html")


@app.route("/account")
@login_required
def profile():
    user = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])[0]

    courses = db.execute(
        "SELECT * FROM profile_items WHERE user_id=? AND category='course'",
        session["user_id"])
    awards = db.execute(
        "SELECT * FROM profile_items WHERE user_id=? AND category='award'",
        session["user_id"])
    extracurriculars = db.execute(
        "SELECT * FROM profile_items WHERE user_id=? AND category='extracurricular'",
        session["user_id"])

    return render_template("account.html", user=user, courses=courses,
                           awards=awards, extracurriculars=extracurriculars)


@app.route("/editprofile", methods=["POST"])
@login_required
def editprofile():
    category = request.form.get("category")
    change = request.form.get("name")

    if not category or not change:
        flash("Pick a category and enter a name")
        return redirect("/account")

    if category == "grade":
        db.execute("UPDATE users SET grade=? WHERE id=?", change, session["user_id"])

    elif category == "sat":
        db.execute("UPDATE users SET sat_score=? WHERE id=?", change, session["user_id"])

    elif category == "act":
        db.execute("UPDATE users SET act_score=? WHERE id=?", change, session["user_id"])

    return redirect("/account")


@app.route("/add_item", methods=["POST"])
@login_required
def add_item():
    category = request.form.get("category")
    name = request.form.get("title")
    description = request.form.get("description")   # must read it

    db.execute("INSERT INTO profile_items (user_id, category, name, description) VALUES(?, ?, ?, ?)",
               session["user_id"], category, name, description)

    return redirect("/account")

@app.route("/delete_item", methods=["POST"])
@login_required
def delete_item():
    item_id = request.form.get("item_id")
    print("DEBUG delete:", repr(item_id))

    db.execute("DELETE FROM profile_items WHERE id=? AND user_id=?",
               item_id, session["user_id"])

    return redirect("/account")

@app.route("/delete_goal", methods=["POST"])
@login_required
def delete_goal():
    item_id = request.form.get("item_id")

    db.execute("DELETE FROM dashboard_items WHERE id=? AND user_id=?",
               item_id, session["user_id"])

    return redirect("/planning")


@app.route("/planning")
@login_required
def planning():
    g9 = db.execute(
        "SELECT * FROM dashboard_items WHERE user_id=? AND grade_level='9'",
        session["user_id"])
    g10 = db.execute(
        "SELECT * FROM dashboard_items WHERE user_id=? AND grade_level='10'",
        session["user_id"])
    g11 = db.execute(
        "SELECT * FROM dashboard_items WHERE user_id=? AND grade_level='11'",
        session["user_id"])
    g12 = db.execute(
        "SELECT * FROM dashboard_items WHERE user_id=? AND grade_level='12'",
        session["user_id"])

    return render_template("planning.html", g9=g9, g10=g10, g11=g11, g12=g12)


@app.route("/addgoal", methods=["POST"])
@login_required
def addgoal():
    grade = request.form.get("grade")
    name = request.form.get("goal")
    
    if not grade or not name:
        flash("Select a grade and enter a goal")
        return redirect("/planning")

    db.execute("INSERT INTO dashboard_items (user_id, grade_level, name) VALUES(?, ?, ?)",
               session["user_id"], grade, name)

    return redirect("/planning")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            flash("Must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return render_template("login.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], request.form.get("password")
        ):
            flash("invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Must provide username")
            return render_template("register.html")
        if not password:
            flash("Must provide password")
            return render_template("register.html")
        if not confirmation:
            flash("Must provide confirmation")
            return render_template("register.html")

        if password != confirmation:
            flash("passwords do not match")
            return render_template("register.html")

        try:
            db.execute("INSERT INTO users (username, password_hash) VALUES(?, ?)",
                       username, generate_password_hash(password))
        except ValueError:
            flash("username already exists")
            return render_template("register.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")
