from flask_login import UserMixin
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

#n to n relationship table for users and customer tables
project = db.Table('projects',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('kunde_id', db.Integer, db.ForeignKey('kunden.kunde_id'))
)

# Zscaler Kunde
class Kunde(db.Model):

    __tablename__ = 'kunden'

    kunde_id = db.Column(db.Integer, primary_key=True, autoincrement="auto")

    def get_id(self):
        return (self.kunde_id)

    kundenname = db.Column(db.String(256), nullable=False)
    api_key = db.Column(db.String(100), nullable=False, unique=True)
    cloud = db.Column(db.String(100), nullable=False)
    customer_domain = db.Column(db.String(100), nullable=False)
    
    user = db.relationship("User", secondary=project, lazy='subquery', backref=db.backref('kunden', lazy=True))

    def __repr__(self):
        return f"<Kunde {self.kundenname}>"

# Login User
class User(UserMixin, db.Model):

    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto") # primary keys are required by SQLAlchemy

    def get_id(self):
        return (self.user_id)
    
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False)
    

    def __repr__(self):
        return f"<User {self.name}>"

# Admin Portal User
class Admin(db.Model):

    __tablename__ = "admins"
    admin_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto") # primary keys are required by SQLAlchemy

    def get_id(self):
        return (self.admin_id)
    
    kunde_id = Column(Integer, ForeignKey("kunden.kunde_id"))
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False) 

    kunde = db.relationship("Kunde", backref=db.backref("admins", lazy=True))

    def __repr__(self):
        return f"<Admin {self.surname} {self.name}>"


# Locations Table
class Location(db.Model):

    __tablename__ = "locations"
    location_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto") # primary keys are required by SQLAlchemy

    def get_id(self):
        return (self.location_id)

    kunde_id = Column(Integer, ForeignKey("kunden.kunde_id"))
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    tz = db.Column(db.String(100), nullable=False)
    vpn_creds_id = db.Column(db.Integer, nullable=False)
    vpn_creds_type = db.Column(db.String(100), nullable=False)
    ofwEnabled = db.Column(db.Boolean)
    ipsControl = db.Column(db.Boolean)
    authRequired = db.Column(db.Boolean)
    xffForwardEnabled = db.Column(db.Boolean)
    profile = db.Column(db.String(100))
    description = db.Column(db.String(256))

    location = db.relationship("Kunde", backref=db.backref("locations"))

    def __repr__(self):
        return f"<Location {self.name}>"

#n to n relationship table for location group and locations tables
mapp_loc_locgroup = db.Table('mapp_loc_locgroups',
    db.Column('locgroup_id', db.Integer, db.ForeignKey('locationgroups.locgroup_id')),
    db.Column('location_id', db.Integer, db.ForeignKey('locations.location_id'))
)

#n to n relationship table for location group and sublocations tables
mapp_loc_sublocgroup = db.Table('mapp_loc_sublocgroups',
    db.Column('locgroup_id', db.Integer, db.ForeignKey('locationgroups.locgroup_id')),
    db.Column('sublocation_id', db.Integer, db.ForeignKey('sublocations.sublocation_id'))
)

# Location Group Table
class LocationGroup(db.Model):

    __tablename__ = "locationgroups"
    locgroup_id  = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto") # primary keys are required by SQLAlchemy

    def get_id(self):
        return (self.locgroup_id )

    name = db.Column(db.String(100), nullable=False)
    typ = db.Column(db.String(100))
    description = db.Column(db.String(256))

    def __repr__(self):
        return f"<Location {self.name}>"

# Sublocation Table
class Sublocation(db.Model):

    __tablename__ = "sublocations"
    sublocation_id  = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto") # primary keys are required by SQLAlchemy

    def get_id(self):
        return (self.sublocation_id )

    location_id = Column(Integer, ForeignKey("locations.location_id"))
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    tz = db.Column(db.String(100), nullable=False)
    vpn_creds_id = db.Column(db.Integer, nullable=False)
    vpn_creds_type = db.Column(db.String(100), nullable=False)
    ofwEnabled = db.Column(db.Boolean)
    ipsControl = db.Column(db.Boolean)
    authRequired = db.Column(db.Boolean)
    xffForwardEnabled = db.Column(db.Boolean)
    profile = db.Column(db.String(100))
    description = db.Column(db.String(256))

    sublocation = db.relationship("Location", backref=db.backref("sublocations"))

    def __repr__(self):
        return f"<Sublocation {self.name}>"

def init_defaults():
    if User.query.first() is None:
        new_user = User(email='georg.loeffler@telekom.de', name='Löffler', surname='Georg', password=generate_password_hash('hallo123', method='sha256'), is_admin=True)
        db.session.add(new_user)
        db.session.commit()
    pass
    if Kunde.query.first() is None:
        new_kunde = Kunde(kundenname='Evangelische Stiftung Alsterdorf', api_key='gF3zlduB9oXf',  cloud='zsapi.zscaler.net', customer_domain='alsterdorf.de')
        db.session.add(new_kunde)
        db.session.commit()
        new_project = project.insert().values(user_id=1, kunde_id=1)
        db.session.execute(new_project)
        db.session.commit()
    pass
    #if Admin.query.first() is None:
    #    new_admin = Admin(kunde_id=1, email='georg.loeffler@alsterdorf.de', password=generate_password_hash('hallo123', method='sha256'), name='Löffler', surname='Georg')
    #    db.session.add(new_admin)
    #    db.session.commit()
    #pass
