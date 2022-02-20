import bcrypt
from flask import Flask, render_template, request, redirect, url_for,session
from dynatransit import db, loginManager, app
from dynatransit.models import User, Trip
from geopy.geocoders import Nominatim
from functools import wraps
import json

from .utils import BusStops_API
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
        
        #time ranges:
        arrivalTimeRangeStart = form.arrivalTimeFrom.data
        arrivalTimeRangeEnd = form.arrivalTimeTo.data
        
        departureTimeRangeStart = form.startTimeFrom.data
        departureTimeRangeEnd = form.startTimeTo.data
                
        departureDate = form.date.data
        
        lat1=currentLocation.latitude
        long1=currentLocation.longitude
        lat2=destinationLocation.latitude
        long2=destinationLocation.longitude
        newTrip = Trip(arrivalLocation=currentAddress, arrivalLong=long1, arrivalLat=lat1, departureLocation=destinationAddress, departureLong=long2, departureLat=lat2, 
                       arrivalTimeRangeStart=str(arrivalTimeRangeStart), arrivalTimeRangeEnd=str(arrivalTimeRangeEnd), 
                       departureTimeRangeStart=str(departureTimeRangeStart), departureTimeRangeEnd=str(departureTimeRangeEnd), departureDate=departureDate, userID=0)
        db.session.add(newTrip)
        db.session.commit()
        #return str(lat1) + " " + str(long1) + " " + str(lat2) + " " + str(long2)
        return render_template('map.html',lat1=lat1,long1=long1,lat2=lat2,long2=long2)
    return render_template('select.html',form=form)

@app.route("/routeview", methods=['GET', 'POST'])
def routeview():
    destinations = BusStops_API.example()
    print(destinations)
    return render_template('route.html',destinationList = json.dumps(destinations))
