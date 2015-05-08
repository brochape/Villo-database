from flask import Flask, request, session, redirect, url_for, jsonify, abort
app = Flask(__name__)
app.testing=True
import os
from functools import wraps
# TODO secret key secured ?
Flask.secret_key = os.urandom(512)
from collections import OrderedDict

import helpers as Helpers

import users as Users
import trips as Trips
import bicycles as Bicycles
import stations as Stations
import billing as Billing

navigation_menu = OrderedDict()

def set_navigation_menu(mode):
    global navigation_menu
    navigation_menu = OrderedDict()
    if mode == "public":
        navigation_menu['Map'] = 'gmap'
        navigation_menu['Login'] = 'login'
        navigation_menu['Register'] = 'register'
    elif mode == "user":
        navigation_menu["Home"] = 'home'
        navigation_menu["Map"] = 'gmap_user'
        navigation_menu["Trips"] = 'trips'
        navigation_menu["Logout"] = 'logout'
    elif mode == "admin":
        navigation_menu["Home"] = 'home'
        navigation_menu["Map"] = 'gmap_user'
        navigation_menu["Trips"] = 'trips'
        navigation_menu["Bicycles"] = "bicycles"
        navigation_menu["Billing"] = "billing"
        navigation_menu["Users"] = "users"
        navigation_menu["Logout"] = 'logout'

set_navigation_menu('public')

def render_template(*args, **kwargs):
    import flask
    return flask.render_template(*args, navigation_menu=navigation_menu, **kwargs)

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
    if "user" in session:
        redirect(url_for('home'))
    if request.method == "GET":
        if "redirect_url" in request.values:
            return render_template("login.html", redirect_url=request.values["redirect_url"])
        else:
            return render_template("login.html")
        
    elif request.method == "POST":
        if Users.login(request.values["user"], request.values["password"]):
            session["user"] = request.values["user"]
            if Users.isAdmin(session["user"]):
                set_navigation_menu('admin')
            else:
                set_navigation_menu('user')
            if "redirect_url" in request.values:
                return redirect(request.values["redirect_url"])
            else:
                return redirect(url_for('home'))
        else:
            return render_template("login.html", error="Incorrect user ID or password")

@app.route("/gmap", methods=['get'])
def gmap():
    if "user" in session:
        return redirect(url_for('gmap_user'))
    else:
        myStations = Stations.query_all()
        return render_template('gmap.html', stationList=myStations)

@app.route("/gmap_user", methods=['get', 'post'])
@require_login
def gmap_user():
    if request.method == "GET":
        myStations = Stations.query_all()
        return render_template('gmap_user.html', stationList=myStations, travelling=Users.isTravelling(session["user"]))
    elif request.method == "POST":
        if "id" not in request.values:
            return abort(400)
        if Users.isTravelling(session["user"]):
            Stations.put_bicycle(int(session["user"]), int(request.values["id"]))
        else:
            Stations.take_bicycle(int(session["user"]), int(request.values["id"]))
        return redirect(url_for('gmap_user'))

@app.route("/logout", methods=['get'])
@require_login
def logout():
    del session["user"]
    set_navigation_menu('public')
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

@app.route("/", methods=['get', 'post'])
@require_login
def home():
    if request.method == "GET":
        expirydate = Users.get_expiry_date(session["user"])[0]
        return render_template("home.html", date=expirydate)
    elif request.method == "POST":
        Users.reNewSub(session["user"])
        return redirect(url_for('home'))

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

@app.route("/bicycles_admin", methods=['get','post'])
@require_login
@require_admin
def bicycles():
    if request.method == "GET":
        mybicycles = Bicycles.select_broken()
        return render_template("bicycles_admin.html", bicycles=mybicycles)
    elif request.method == "POST":
        bicycleID = request.values["id"]
        Bicycles.repair(bicycleID)
        mybicycles = Bicycles.select_broken()
        return redirect(url_for('bicycles'))


@app.route("/stations", methods=['get'])
def stations():
    results = Stations.query_all()
    return jsonify(data=results)

@app.route("/billing", methods=['get', 'post'])
@require_login
@require_admin
def billing():
    if request.method == "GET":
        return render_template("billing.html")
    elif request.method == "POST":
        if not "month" in request.values or not "year" in request.values:
            return abort(400)
        try:
            int(request.values["month"])
            int(request.values["year"])
        except:
            return render_template("billing.html")
        if request.values["month"] == "00":
            date = request.values["year"]
        else:
            date = request.values["month"] + "/" + request.values["year"]
        data = {}
        data["subs"] = Billing.subscribers(date)
        data["temp"] = Billing.tempUsers(date)
        data["billing_subs"] = Billing.billing_subscribers(date)
        data["billing_temp"] = Billing.billing_tempusers(date)
        data["billing_trips"] = Billing.billing_trips(date)
        return render_template("billing.html", data=data)

@app.route("/users", methods=['get'])
@require_login
@require_admin
def users():
    return ""

app.run('0.0.0.0', debug=True)