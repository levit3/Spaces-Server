#!/usr/bin/env python3
from flask import request, make_response, session, jsonify
from flask_restful import Resource
import cloudinary
import jwt
from functools import wraps
from datetime import datetime, timedelta

from config import app, db, api
from models import User, Review, Space, Payment ,Booking, ReviewImage
import cloudinary.uploader
import cloudinary.api



cloudinary.config(
  cloud_name = 'dzqt3usfp',
  api_key = '618183139173486',
  api_secret = '6oUAsFqSzho3xOjxebi3SIUps9U'
)

@app.route('/')
def index():
    return "Welcome to Spaces."

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return make_response('Token is missing', 401)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
            if not current_user:
                return make_response(jsonify({'message': 'User not found'}), 401)
            
            expiration = datetime.fromisoformat(data.get('expiration', ''))
            if expiration < datetime.utcnow():
                return make_response('Token expired', 401)
        except jwt.ExpiredSignatureError:
            return make_response('Token expired', 401)
        except jwt.InvalidTokenError:
            return make_response('Invalid token', 401)

        return func(*args, **kwargs, current_user=current_user)

    return decorated



class Bookings(Resource):
    def get(self):
        booking = Booking.query.all()
        return booking.to_dict()
    
class BookingByID(Resource):
    def get(self, booking_id):
        booking = Booking.query.filter_by(id=booking_id).first()
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


class Users(Resource):
    def get(self):
        users = User.query.all()
        user = [user.to_dict() for user in users]
        return make_response(user)
    

class UserByID(Resource):
    @token_required
    def get(self, user_id, current_user):
        if current_user.id != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        user = User.query.filter_by(id = user_id).first()
        return make_response(user.to_dict(), 200)
    
    @token_required      
    def put(self, user_id):
        user = User.query.get(user_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user.to_dict()

    @token_required      
    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return user.to_dict()
    
    @token_required      
    def patch(self, user_id):
        user = User.query.get(user_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user.to_dict()
    


class Reviews(Resource):
    def get(self):
        review = Review.query.all()
        return review.to_dict()
    
class ReviewByID(Resource):
    def get(self, review_id):
        review = Review.query.get_or_404(review_id)
        return review.to_dict(), 200
    
    @token_required
    def put(self, review_id):
        review = Review.query.get_or_404(review_id)
        data = request.form
        images = request.files.getlist('images')  
        
        try:
            
            for key, value in data.items():
                setattr(review, key, value)
            
            
            if images:
                for image in images:
                    upload_result = cloudinary.uploader.upload(image)
                    review_image = ReviewImage(image_url=upload_result['url'])
                    review.images.append(review_image)

            db.session.commit()
            return review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @token_required
    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted'}, 200
    
    @token_required
    def patch(self, review_id):
        review = Review.query.get_or_404(review_id)
        data = request.form
        images = request.files.getlist('images') 
        
        try:
            
            for key, value in data.items():
                setattr(review, key, value)
            
            
            if images:
                for image in images:
                    upload_result = cloudinary.uploader.upload(image)
                    review_image = ReviewImage(image_url=upload_result['url'])
                    review.images.append(review_image)

            db.session.commit()
            return review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

class Payments(Resource):
    #@token_required      
    def get(self):
        payments = Payment.query.all()
        payment = [payment.to_dict() for payment in payments]
        return payment
    
    
class PaymentByID(Resource):
    # @token_required      
    def get(self, payment_id):
        payment = Payment.query.get(payment_id)
        return payment.to_dict()

    @token_required      
    def put(self, payment_id):
        payment = Payment.query.get(payment_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(payment, key, value)
        db.session.commit()
        return payment.to_dict()

    @token_required   
    def delete(self, payment_id):
        payment = Payment.query.get(payment_id)
        db.session.delete(payment)
        db.session.commit()
        return payment.to_dict()

    @token_required
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
      return make_response((space_data), 200)

class SpaceByID(Resource):
    #@token_required
    def get(self, space_id):
        space = Space.query.get(space_id)
        return [space.to_dict()]

    @token_required
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

    @token_required   
    def put(self, space_id):
        space = Space.query.get(space_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(space, key, value)
        db.session.commit()
        return space.to_dict()

    @token_required   
    def delete(self, space_id):
       space = Space.query.get(space_id)
       db.session.delete(space)
       db.session.commit()
       return space.to_dict()

    @token_required   
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

        name = request_json.get('name')
        password = request_json.get('password')

        user = User.query.filter(User.name == name).first()

        if user:
            if user.authenticate(password):
                session['user_id'] = user.id
                token = jwt.encode({'id': user.id, 'expiration': str(datetime.utcnow()+timedelta(days=5))}, app.config['SECRET_KEY'],algorithm="HS256")
                return make_response({'user': user.to_dict(), 'token': token}, 200)
            else:
                return {'error': 'Invalid Password'}, 401

        return {'error': 'Invalid Username'}, 401

class Logout(Resource):

    def delete(self):

        session['user_id'] = None
        
        return {}, 204

class CheckSession(Resource):
 def get():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Unauthorized"}), 401

api.add_resource(CheckSession, '/api/check_session')   
api.add_resource(Payments, '/api/payments')
api.add_resource(PaymentByID, '/api/payments/<int:payment_id>/')
api.add_resource(Reviews, '/api/reviews')
api.add_resource(ReviewByID, '/api/reviews/<int:review_id>/')
api.add_resource(Users, '/api/users')
api.add_resource(UserByID, '/api/users/<int:user_id>/')
api.add_resource(Bookings, '/api/bookings')
api.add_resource(BookingByID, '/api/bookings/<int:booking_id>/')
api.add_resource(Spaces, '/api/spaces>')
api.add_resource(SpaceByID, '/api/spaces/<int:space_id>/')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')

if __name__ == '__main__':
    app.run(port= 5555, debug=True)



