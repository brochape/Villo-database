from flask import Flask, request, render_template, session, redirect, url_for, jsonify
app = Flask(__name__)
app.testing=True
import os
from functools import wraps
# TODO secret key secured ?
Flask.secret_key = os.urandom(512)

import users as Users
import trips as Trips
import bicycles as Bicycles
import stations as Stations

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

@app.route("/gmap", methods=['get'])
def gmap():
    myStations = Stations.query_all()
    return render_template('gmap.html', stationList=myStations)

@app.route("/gmap_user", methods=['get', 'post'])
@require_login
def gmap_user():
    if request.method == "GET":
        myStations = Stations.query_all()
        return render_template('gmap_user.html', stationList=myStations)
    elif request.method == "POST":
        if "id" not in request.values:
            return abort(400)
        Stations.take_bicycle(session["user"], request.values["id"])# TODO:Reste a savoir quel station est celle consideree
        return redirect(url_for('gmap_user'))

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
    if request.method == "GET":
        return render_template("home.html")

@app.route("/trips", methods=['get'])
@require_login
def trips():
    myTrips = Trips.query_all(session["user"])
    return render_template("trips.html", trips=myTrips)

@app.route("/bicycle", methods=['get', 'post'])
@require_login
def bicycle():
    if "id" not in request.values:
        return abort(400)
    bicycleID = request.values["id"]
    # show bicycle information
    if request.method == "GET":
        result = Bicycles.select(bicycleID)
        if not result:
            return abort(400)
        result["id"] = bicycleID
        result["state"] = "No" if result["state"] == 0 else "Yes"
        if result["state"] == "Yes":
            result["repair"] = True
        else:
            pass
        return render_template("bicycle.html", bicycle=result)
    # report broken bicycle
    elif request.method == "POST":
        Bicycles.report(bicycleID)
        return redirect(url_for('bicycle', id=bicycleID))

@app.route("/stations", methods=['get'])
def stations():
    results = Stations.query_all()
    return jsonify(data=results)

@app.route("/billing", methods=['get'])
@require_login
@require_admin
def billing():
    return ""

@app.route("/users", methods=['get'])
@require_login
@require_admin
def users():
    return ""

app.run('0.0.0.0', debug=True)