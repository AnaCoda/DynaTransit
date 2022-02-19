import bcrypt
from flask import Flask, render_template, request, redirect, url_for
from dynatransit import db, loginManager, app
from geopy.geocoders import Nominatim
from functools import wraps

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
    if request.method == 'POST':
        currentAddress = request.form['current-address']
        currentLocation = geolocator.geocode(currentAddress)
        
        destinationAddress = request.form['destination-address']
        destinationLocation = geolocator.geocode(destinationAddress)
        
        lat1=currentLocation.latitude
        long1=currentLocation.longitude
        lat2=destinationLocation.latitude
        long2=destinationLocation.longitude
        #return str(lat1) + " " + str(long1) + " " + str(lat2) + " " + str(long2)
        return render_template('map.html',lat1=lat1,long1=long1,lat2=lat2,long2=long2)
    return render_template('select.html')
