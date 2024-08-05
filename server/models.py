from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import func
from config import db, bcrypt
import re

##Users

class UserRole(enum.Enum):
    USER = "user"
    TENANT = "tenant"
    ADMIN = "admin"

class User( SerializerMixin, db.Model):
    __tablename__ = 'users'

    serialize_rules = ['-spaces.user', '-reviews.user', '-bookings.user', '-payments.payments', '-spaces.reviews', '-reviews.space.user', '-bookings.payment.booking']
       
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)
    role = db.Column(db.Enum(UserRole), nullable=False)
    
    spaces = db.relationship('Space', back_populates = 'user')
    reviews = db.relationship("Review", back_populates = 'user')
    bookings = db.relationship("Booking", back_populates = 'user')
    payments = association_proxy('bookings','payments')


    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name}, role={self.role})>"
    
    @hybrid_property
    def password(self):
      return self._password

    @password.setter
    def password(self, password):
        if (
        len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"[0-9]", password) or
        not re.search(r"[\W_]", password)
    ):
            raise ValueError(
            'Password MUST be at least 8 digits, include uppercase, lowercase, numbers & special characters.'
        )

        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password, password.encode('utf-8'))

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+.[^@]+", email):
                        raise ValueError('Invalid email address')
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            raise ValueError('Email already exists')
        return email


##Spaces

class Space(db.Model, SerializerMixin):
    __tablename__ ='spaces'
    
    serialize_rules = ['-user.spaces', '-bookings.space', '-reviews.space', '-user.reviews', '-user.bookings', '-reviews.user','-bookings.user.spaces', '-bookings.payment.booking', '-bookings.payment.booking', '-bookings.user.reviews', '-bookings.user.bookings', '-bookings.user.payments']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates = 'spaces')
    reviews = db.relationship('Review', back_populates ='space')
    space_images = db.relationship('SpaceImages', back_populates='space')
    bookings = db.relationship('Booking', back_populates='space')


    def __repr__(self):
        return f'<Space {self.title} description: {self.description}>'
    
class SpaceImages(db.Model, SerializerMixin):
    __tablename__ = 'space_images'

    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=False)
    image_url = db.Column(db.String, nullable=False)

    space = db.relationship('Space', back_populates='space_images')

    def __repr__(self):
        return f'<SpaceImage {self.image_url}>'


#Bookings
class Booking(db.Model,SerializerMixin):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    updated_at = db.Column(db.Date, nullable=True)
    
   
    serialize_rules=["-space.bookings","-user.bookings","-payment,booking"]
    
    user = db.relationship('User', back_populates='bookings')
    payment=db.relationship('Payment', back_populates='booking')
    space = db.relationship('Space', back_populates='bookings')

#Reviews
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    serialize_rules = ['-space.reviews', '-user.reviews', '-space.user']
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=False)
    date = db.Column(db.Date, server_default=func.current_date())
    
    images = db.relationship('ReviewImage', back_populates='review', cascade='all, delete-orphan')
    space = db.relationship('Space', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
  
    def __repr__(self):
        return f'<Review {self.rating}, {self.comment}, {self.user_id}, {self.space_id}>'
  
    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError('Rating must be between 1 and 5')
        return rating
  
    @validates('space_id')
    def validate_space_id(self, key, space_id):
        space = Space.query.get(space_id)
        if not space:
            raise ValueError('Space does not exist')
        return space_id
  
    @validates('comment')
    def validate_comment(self, key, comment):
        if len(comment) < 5:
            raise ValueError('Comment must be at least 5 characters long')
        return comment

class ReviewImage(db.Model, SerializerMixin):
    __tablename__ = 'review_images'
    
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    image_url = db.Column(db.String, nullable=False) 
    
    review = db.relationship('Review', back_populates='images')
    
    def __repr__(self):
        return f'<ReviewImage {self.image_url}>'


#Payments
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    payment_status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.current_date())
    
    serialize_rules = ['-booking.payments', '-booking.user.spaces', '-booking.user.reviews']
    
    booking = db.relationship("Booking", back_populates="payment")
    user = association_proxy('booking', 'user')
    
    def __repr__(self):
        return f"<Payment(id={self.id}, booking_id={self.booking_id}, amount={self.amount}, payment_method='{self.payment_method}', payment_status='{self.payment_status}', created_at={self.created_at})>"
    
    @validates('booking_id')
    def validate_booking_id(self, key, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            raise ValueError('Booking does not exist')
        return booking_id
    @validates('amount')
    def validate_amount(self, key, amount):
        if amount < 0:
            raise ValueError('Amount must be greater than 0')
        return amount