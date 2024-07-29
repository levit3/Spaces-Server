from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from config import db, bcrypt
from datetime import datetime
##Users














##Spaces
class Spaces(db.Model, SerializerMixin):
    __tablename__ ='spaces'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tenant = db.relationship('User', back_populates = 'spaces')

    def __repr__(self):
        return f'<Space {self.title}, {self.description}>'
 










#Bookings




















#Reviews












#Payments
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    payment_status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    booking = db.relationship("Booking", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment(id={self.id}, booking_id={self.booking_id}, amount={self.amount}, payment_method='{self.payment_method}', payment_status='{self.payment_status}', created_at={self.created_at})>"