#!/usr/bin/env python3
from flask import request, make_response
from flask_restful import Resource

from config import app, db, api
from models import User, Review, Space, Payment ,Booking


app.route('/')
def index():
    return "Welcome to Spaces."

class Bookings(Resource):
    def get(self, booking_id):
        booking = Booking.query.get(booking_id).first()
        return booking.to_dict()

    def put(self, booking_id):
        booking = Booking.query.get(booking_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(booking, key, value)
        db.session.commit()
        return booking.to_dict()

    def delete(self, booking_id):
        booking = Booking.query.get(booking_id)
        db.session.delete(booking)
        db.session.commit()
        return booking.to_dict()

    def patch(self, booking_id):
        booking = Booking.query.get(booking_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(booking, key, value)
        db.session.commit()
        return booking.to_dict()
api.add_resource(Booking, '/api/bookings/<int:booking_id>')

class User(Resource):
    def get(self, user_id):
        user = User.query.get(user_id).first()
        return user.to_dict()
    
    def put(self, user_id):
        user = User.query.get(user_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user.to_dict()

    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return user.to_dict()

api.add_resource(User, '/api/users/<int:user_id>')





  