import bcrypt
from flask import Flask, render_template, request, redirect, url_for,session,flash
from dynatransit import db, loginManager, app
from dynatransit.models import User, Trip
from geopy.geocoders import Nominatim
from shapely.geometry import Point
from functools import wraps
import json

from .utils import BusStops_API
from dynatransit.forms import RegistrationForm, LoginForm, FindTrip

geolocator = Nominatim(user_agent="app")

def LoginRequired(f):
    #this would be the function that is being decorated 
    @wraps(f)
    def wrap(*args, **kwargs):
        if "loggedIn" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first", "danger")
            return redirect(url_for("login"))
    return wrap

@app.route("/")
@app.route("/home")
def home():
    if "loggedIn" in session:
        return redirect(url_for('mapview'))
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(str(form.password.data).encode('utf8'), bcrypt.gensalt())
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        session["loggedIn"] = True
        session["emailID"] = form.email.data
        session["username"] = User.query.filter_by(email=form.email.data).first().username
        return redirect(url_for('mapview'))
    return render_template('register.html', form=form)

@app.route("/logout")
def logout():
    session.clear()
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():   
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8') ,user.password):
            session['loggedIn'] = True
            session["emailID"] = form.email.data
            session["username"] = User.query.filter_by(email=form.email.data).first().username
            flash(f"You are now logged in, {user.username}", "success")
            return redirect(url_for('mapview'))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template('login.html',form=form)

@app.route("/mapview", methods=['GET', 'POST'])
@LoginRequired
def mapview():
    form = FindTrip()
    if form.validate_on_submit():   
        currentAddress = form.start.data
        currentLocation = geolocator.geocode(currentAddress)
        
        destinationAddress = form.end.data
        destinationLocation = geolocator.geocode(destinationAddress)
        
        #time ranges:
        arrivalTimeRangeStart = form.arrivalTimeFrom.data
        arrivalTimeRangeEnd = form.arrivalTimeTo.data
                
        departureDate = form.date.data
        
        lat1=currentLocation.latitude
        long1=currentLocation.longitude
        lat2=destinationLocation.latitude
        long2=destinationLocation.longitude
        newTrip = Trip(arrivalLocation=currentAddress, arrivalLong=long1, arrivalLat=lat1, departureLocation=destinationAddress, departureLong=long2, departureLat=lat2, 
                       arrivalTimeRangeStart=str(arrivalTimeRangeStart), arrivalTimeRangeEnd=str(arrivalTimeRangeEnd), 
                    departureDate=departureDate, userID=0)
        db.session.add(newTrip)
        db.session.commit()
        #return str(lat1) + " " + str(long1) + " " + str(lat2) + " " + str(long2)
        return render_template('map.html',lat1=lat1,long1=long1,lat2=lat2,long2=long2,username=session["username"])
    return render_template('select.html',form=form,lat1=51.0447,long1=-114.0719,username=session["username"])


@app.route("/routeview", methods=['GET', 'POST'])
def routeview():
    results = Trip.query.with_entities(Trip.arrivalLong, Trip.arrivalLat, Trip.departureLong, Trip.departureLat).all()
        
    realPoints = []
    for coord in results:
        realPoints.append(Point(coord[1], coord[0]))
        realPoints.append(Point(coord[3], coord[2]))
    
    destinations = BusStops_API.findStops(realPoints)
    print(destinations)
    return render_template('route.html',destinationList = json.dumps(destinations))