import bcrypt
from flask import Flask, render_template, request, redirect, url_for,session
from dynatransit import db, loginManager, app
from dynatransit.models import User, Trip
from geopy.geocoders import Nominatim
from functools import wraps
from dynatransit.forms import RegistrationForm, LoginForm, FindTrip

geolocator = Nominatim(user_agent="app")

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/mapview", methods=['GET', 'POST'])
def mapview():
    form = FindTrip()
    if form.validate_on_submit():   

        currentAddress = form.start.data
        currentLocation = geolocator.geocode(currentAddress)
        
        destinationAddress = form.end.data
        destinationLocation = geolocator.geocode(destinationAddress)
        
        #time ranges
        #departureTime = request.form['departure-time']
        #arrivalTime = request.form['arrival-time']
        
        #departureDate = request.form['departure-date']
        
        lat1=currentLocation.latitude
        long1=currentLocation.longitude
        lat2=destinationLocation.latitude
        long2=destinationLocation.longitude
        
        newTrip = Trip(arrivalLocation=currentAddress, arrivalLong=long1, arrivalLat=lat1, departureLocation=destinationAddress, departureLong=long2, departureLat=lat2, 
                       arrivalTimeRangeStart=0, arrivalTimeRangeEnd=0, departureTimeRangeStart=0, departureTimeRangeEnd=0, departureDate=0, userID=0)
        
        #return str(lat1) + " " + str(long1) + " " + str(lat2) + " " + str(long2)
        return render_template('map.html',lat1=lat1,long1=long1,lat2=lat2,long2=long2)
    return render_template('select.html',form=form)
