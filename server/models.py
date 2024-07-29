from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import re
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from config import db, bcrypt
##Users

Base = declarative_base()
class UserRole(enum.Enum):
    USER = "user"
    TENANT = "tenant"

class User(Base):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)
    role = db.Column(db.Enum(UserRole), nullable=False)
    spaces = db.relationship("Space", back_populates = 'user')
    

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name}, role={self.role})>"      

##Spaces
class Space(db.Model, SerializerMixin):
    __tablename__ ='spaces'
    
    serialize_rules = ('-user.spaces', '-bookings.space', '-reviews.space')
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tenant = db.relationship('User', back_populates = 'spaces')
    bookings = db.relationship('Booking', back_populates ='space')
    reviews = db.relationship('Review', back_populates ='space')


    def __repr__(self):
        return f'<Space {self.title}, {self.description}>'

 










#Bookings




















#Reviews












#Payments