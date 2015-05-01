from flask import Flask, request, render_template, session, redirect, url_for
app = Flask(__name__)
app.testing=True
import os
from functools import wraps
# TODO secret key secured ?
Flask.secret_key = os.urandom(512)

import users as Users

def require_login(f):
    @wraps(f)
    def g(*args, **kwargs):
        if "user" not in session:
        	return redirect(url_for('login', redirect_url=request.url))
        else:
            return f(*args, **kwargs)
    return g

def require_admin(f):
	@wraps(f)
	def g(*args, **kwargs):
		if Users.isAdmin(session["user"]):
			return f(*args, **kwargs)
		else:
			return redirect(url_for('home'))
	return g

@app.route("/login", methods=['get', 'post'])
def login():
	if request.method == "GET":
		if "redirect_url" in request.values:
			return render_template("login.html", redirect_url=request.values["redirect_url"])
		else:
			return render_template("login.html")
		
	elif request.method == "POST":
		if Users.login(request.values["user"], request.values["password"]):
			session["user"] = request.values["user"]
			if "redirect_url" in request.values:
				return redirect(request.values["redirect_url"])
			else:
				return redirect(url_for('home'))
		else:
			return render_template("login.html", error="Incorrect user ID or password")

@app.route("/logout", methods=['get'])
@require_login
def logout():
	del session["user"]
	return redirect(url_for('login'))

@app.route("/register", methods=['get', 'post'])
def register():
	if request.method == "GET":
		return render_template("register.html")
	elif request.method == "POST":
		errors = Users.register(request.values)
		if errors:
			return render_template("register.html", errors=errors, values=request.values)
		else:
			return redirect(url_for('login'))

@app.route("/home", methods=['get'])
@require_login
def home():
	return ""

@app.route("/trips", methods=['get'])
@require_login
def trips():
	return ""

@app.route("/users", methods=['get'])
@require_login
@require_admin
def users():
	return ""

app.run('0.0.0.0', debug=True)