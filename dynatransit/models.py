from dynatransit import db, loginManager

@loginManager.user_loader
def loadUser(userID):
    return User.query.get(int(userID))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)    
    events = db.relationship("Event", backref="user", lazy=True)
    
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
    
    arrivalTimeRangeStart = db.Column(db.Float, nullable=False)
    arrivalTimeRangeEnd = db.Column(db.Float, nullable=False)
    
    departureTimeRangeStart = db.Column(db.Float, nullable=False)
    departureTimeRangeEnd = db.Column(db.Float, nullable=False)
    
    departureDate = db.Column(db.DateTime, nullable=False) 
    
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)