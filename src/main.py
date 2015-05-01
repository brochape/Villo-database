from flask import Flask, request, render_template, session, redirect, url_for
app = Flask(__name__)
import os
from functools import wraps
# TODO secret key secured ?
Flask.secret_key = os.urandom(512)

import users

def require_login(f):
    @wraps(f)
    def g(*args, **kwargs):
        if "user" not in session:
        	return redirect(url_for('login', redirect_url=request.url))
        else:
            return f(*args, **kwargs)
    return g

@app.route("/login", methods=['get', 'post'])
def login():
	print request.method
	if request.method == "GET":
		if "redirect_url" in request.values:
			return render_template("login.html", redirect_url=request.values["redirect_url"])
		else:
			return render_template("login.html")
		
	elif request.method == "POST":
		if users.login(request.values["user"], request.values["password"]):
			session["user"] = request.values["user"]
			if "redirect_url" in request.values:
				return redirect(request.values["redirect_url"])
			else:
				return redirect(url_for('home'))
		else:
			# TODO add errors
			return render_template("login.html")

@app.route("/logout", methods=['get'])
@require_login
def logout():
	del session["user"]
	return redirect(url_for('login'))

@app.route("/home", methods=['get'])
@require_login
def home():
	return ""

@app.route("/trips", methods=['get'])
@require_login
def trips():
	return ""

app.run('0.0.0.0', debug=True)