import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    shares_total = 0
    """Show portfolio of stocks"""
    rows = db.execute("SELECT symbol, shares FROM portfolio WHERE id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    cash = round(cash, 2)

    for row in rows:
        quote = lookup(row["symbol"])
        row["price"] = quote["price"]
        row["total"] = row["price"] * row["shares"]
        shares_total += row["total"]

    grand_total = shares_total + cash
    grand_total = round(grand_total, 2)

    return render_template("portfolio.html", rows = rows, cash = cash, grand_total = grand_total)

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == "POST":
        adding = int(request.form.get("add"))
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        cash += adding
        db.execute("UPDATE users SET cash = ? WHERE id=?", cash, session["user_id"])

        return redirect("/")
    return render_template("addcash.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        quote = lookup(symbol)
        if not symbol or quote is None:
            return apology("Provide a symbol")

        if not shares or not shares.isdigit():
            return apology("invalid shares")

        shares = int(shares)
        if shares <= 0:
            return apology("Shares must be a positive number")

        price = quote["price"]
        total_to_buy = round(price * shares, 2)
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if user_cash < total_to_buy:
            return apology("Not enough funds")

        user_cash -= total_to_buy

        # update cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash, session["user_id"])

        # add to history
        db.execute("INSERT INTO history (id, time, price, symbol, share, action) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], datetime.now().isoformat(), price, symbol, shares, "buy")

        # update portfolio
        rows = db.execute("SELECT shares FROM portfolio WHERE id = ? AND symbol = ?", session["user_id"], symbol)

        if len(rows) == 0:
            db.execute("INSERT INTO portfolio (id, symbol, shares) VALUES(?, ?, ?)", session["user_id"], symbol, shares)

        else:
            db.execute("UPDATE portfolio SET shares = shares + ? WHERE id = ? AND symbol = ?", shares, session["user_id"], symbol)

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT time, action, symbol, share, price FROM history WHERE id=?", session["user_id"])

    return render_template("history.html", rows = rows)


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
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol")

        stock = lookup(symbol)

        if stock is None:
            return apology("Invalid symbol")

        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must provide username")
        if not password:
            return apology("Must provide password")
        if not confirmation:
            return apology("Must provide confirmation")

        if password != confirmation:
            return apology("passwords do not match")

        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        except ValueError:
            return apology("username already exists")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Must select symbol")
        if not shares.isdigit():
            return apology("Must select valid shares")
        shares = int(shares)
        if shares <= 0:
            return apology("Must sell 1 or more shares")


        row = db.execute("SELECT shares FROM portfolio WHERE id = ? AND symbol = ?", session["user_id"], symbol)


        if len(row) == 0:
            return apology("You do not own that stock")

        owned_shares = row[0]["shares"]
        if owned_shares < shares:
            return apology("You do not have enough shares")

        # update history
        price = lookup(symbol)["price"]
        db.execute("INSERT INTO history (id, time, price, symbol, share, action) VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], datetime.now().isoformat(), price, symbol, shares, "sell")

        # update cash
        sold_total = price * shares
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        cash += sold_total
        db.execute("UPDATE users SET cash=? WHERE id=?", cash, session["user_id"])

        # update portfolio
        db.execute("UPDATE portfolio SET shares = shares - ? WHERE id=? AND symbol=?", shares, session["user_id"], symbol)

        #delete any rows with 0
        db.execute(
            "DELETE FROM portfolio WHERE id=? AND symbol=? AND shares=0",
            session["user_id"],
            symbol
        )


    else:
        stocks = db.execute(
            "SELECT symbol FROM portfolio WHERE id = ?",
            session["user_id"]
        )

        return render_template("sell.html", stocks = stocks)

    return redirect("/")
