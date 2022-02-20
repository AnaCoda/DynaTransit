from dynatransit import db, loginManager

@loginManager.user_loader
def loadUser(userID):
    return User.query.get(int(userID))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)    
    trips = db.relationship("Trip", backref="user", lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}, {self.email}')"


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    arrivalLocation = db.Column(db.String(200), nullable=False)
    arrivalLong = db.Column(db.Float, nullable=False)
    arrivalLat = db.Column(db.Float, nullable=False)
    
    departureLocation = db.Column(db.String(200), nullable=False)
    departureLong = db.Column(db.Float, nullable=False)
    departureLat = db.Column(db.Float, nullable=False)
    
    arrivalTimeRangeStart = db.Column(db.String(30), nullable=False)
    arrivalTimeRangeEnd = db.Column(db.String(30), nullable=False)
    
    departureTimeRangeStart = db.Column(db.String(30), nullable=False)
    departureTimeRangeEnd = db.Column(db.String(30), nullable=False)
    
    departureDate = db.Column(db.String(200), nullable=False) 
    
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    waypoint = db.Column(db.String(900), nullable=False)
    
    destination = db.Column(db.String(200), nullable=False)

    time = db.Column(db.String(30), nullable=False)

    departureDate = db.Column(db.String(200), nullable=False) 
    
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)