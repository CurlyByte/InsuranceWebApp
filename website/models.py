from . import db
""" importing from root(.) -> db that is created in init )db = Sqlalchemy"""
from flask_login import UserMixin
from datetime import datetime
"""installed pip flask-login so i can define scheme for tables"""
"""creating table wit user, id as primary key, email, """

class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    insurance_name= db.Column(db.String(20))
    amount = db.Column(db.String(100))
    creation_date = db.Column(db.DateTime())
    expiration_date = db.Column(db.DateTime())
    user = db.relationship('User', secondary="insurance_user", back_populates='insurance')
    
    def __str__(self):
        return self.insurance_name
"""creating foreign key"""


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    address = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    insurance = db.relationship('Insurance', secondary="insurance_user", back_populates='user')
    def __str__(self):
        return self.email
    """userinfo is creating a list with userinfo via relationship"""

db.Table(
    "insurance_user",
    db.Column("insurance_id", db.ForeignKey("insurance.id"), primary_key=True),
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True))