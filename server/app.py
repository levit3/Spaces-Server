#!/usr/bin/env python3
from flask import request, make_response, session
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
    


class Payments(Resource):
    def get(self, payment_id):
        payment = Payment.query.get(payment_id).first()
        return payment.to_dict()

    def put(self, payment_id):
        payment = Payment.query.get(payment_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(payment, key, value)
        db.session.commit()
        return payment.to_dict()

    def delete(self, payment_id):
        payment = Payment.query.get(payment_id)
        db.session.delete(payment)
        db.session.commit()
        return payment.to_dict()

    def patch(self, payment_id):
        payment = Payment.query.get(payment_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(payment, key, value)
        db.session.commit()
        return payment.to_dict()
    

class Spaces(Resource):
    def get(self):
      spaces = Space.query.all()
      space_data = [space.to_dict() for space in spaces]
      return make_response(jsonify(space_data), 200)

class Space(Resource):
    def get(self, space_id):
        space = Space.query.get(space_id)
        return [space.to_dict()]

    def post(self):
        data = request.get_json()
        title = data.get('username')
        description = data.get('email')
        location = data.get('password')
        price_per_hour = data.get('balance')
        status = data.get('status')
        
        space = Space(
          title=title,
          description=description,
          location=location,
          price_per_hour=price_per_hour,
          status=status,
        )
        db.session.add(space)
        db.session.commit()
        return space.to_dict()

    def put(self, space_id):
        space = Space.query.get(space_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(space, key, value)
        db.session.commit()
        return space.to_dict()

    def delete(self, space_id):
       space = Space.query.get(space_id)
       db.session.delete(space)
       db.session.commit()
       return space.to_dict()

    def patch(self, space_id):
     space = Space.query.get(space_id)
     data = request.get_json()
     for key, value in data.items():
        setattr(space, key, value)
     db.session.commit()
     return space.to_dict()
    
class Login(Resource):
    
    def post(self):

        request_json = request.get_json()

        username = request_json.get('username')
        password = request_json.get('password')

        user = User.query.filter(User.username == username).first()

        if user:
            if user.authenticate(password):

                session['user_id'] = user.id
                return user.to_dict(), 200

        return {'error': '401 Unauthorized'}, 401

class Logout(Resource):

    def delete(self):

        session['user_id'] = None
        
        return {}, 204
    
api.add_resource(Payments, '/api/payments/<int:payment_id>')
api.add_resource(User, '/api/users/<int:user_id>')
api.add_resource(Booking, '/api/bookings/<int:booking_id>')
# api.add_resource(Reviews, '/api/reviews/<int:review_id>')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(Spaces, '/api/spaces>')

if __name__ == '__main__':
    app.run(port= 5555, debug=True)



