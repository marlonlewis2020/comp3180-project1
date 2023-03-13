from . import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, index=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(30))
    
    def __init__(self, username, password, role):
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.role = role
    

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    bedrooms = db.Column(db.String(3)) 
    bathrooms = db.Column(db.String(3)) 
    location  = db.Column(db.String(80)) 
    price  = db.Column(db.String(18))
    property_type = db.Column(db.String(10))
    description = db.Column(db.String(255))
    photo = db.Column(db.String(128), default="")
    
    def __init__(self, title, bedrooms, bathrooms, location, price, property_type, description, filename):
        self.name = title
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.location = location
        self.price = price
        self.property_type = property_type
        self.description = description
        self.photo = filename
        print(self)

