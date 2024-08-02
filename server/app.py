#!/usr/bin/env python3
from flask import request, make_response, session, jsonify
from flask_restful import Resource
import cloudinary
import jwt
import requests
from functools import wraps
from datetime import datetime, timedelta

from config import app, db, api
from models import User, Review, Space, Payment ,Booking, ReviewImage, Event
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
    
    def post(self):
        data = request.json
        booking = Booking(user_id = data['user_id'], space_id = data['space_id'], start_date = data['start_date'], end_date = data['end_date'], total_price = data['total_price'],status = data['status'], created_at = data['created_at'], updated_at = data['updated_at'])
        db.session.add(booking)
        db.session.commit()
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
    
    def post(self):
        data = request.json
        review = Review(comment=data['comment'], rating=data['rating'], user_id=data['user_id'], space_id=data['space_id'])    
        db.session.add(review)
        db.session.commit()
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
    
    def post(self):
        data = request.get_json()
        payment = Payment(**data)
        db.session.add(payment)
        db.session.commit()
        return payment.to_dict()
    
    
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
      return make_response(jsonify(space_data), 200)
    
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

class SpaceByID(Resource):
    # @token_required
    def get(self, space_id):
        space = Space.query.get(space_id)
        return [space.to_dict()]

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
    
    
class Events(Resource):
    def get(self):
        events = Event.query.all()
        event_data = [event.to_dict() for event in events]
        return make_response(jsonify(event_data), 200)

    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        location = data.get('location')
        date = data.get('date')
        organizer_id = data.get('user_id')
        space_id = data.get('space_id')   

        event = Event(
            title=title,
            description=description,
            location=location,
            date=date,
            organizer_id=organizer_id,
            space_id=space_id)
        db.session.add(event)
        db.session.commit()
        return make_response(event.to_dict())
class EventByID(Resource):
    def get(self, event_id):
        event = Event.query.get(event_id)
        return [event.to_dict()]

    def patch(self, id):
        event = Event.query.get(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(event, key, value)
        db.session.commit()
        return make_response(event.to_dict())

    def delete(self, id):
        event = Event.query.get(id)
        db.session.delete(event)
        db.session.commit()
        return make_response(event.to_dict())  
    
class SendEmail(Resource):
    def post(self):
        data = request.get_json()
        to = data.get('to')

        if not to:
            return {"message": "Recipient email is required"}, 400

        mailjet_api_key = 'c40b5166cf91591dfd94b42e4d944ec8'
        mailjet_secret_key = '63d83d87e6f22984189b90a177907ce7'
        mailjet_url = 'https://api.mailjet.com/v3.1/send'

        headers = {
            'Content-Type': 'application/json'
        }

        email_data = {
            'Messages': [
                {
                    'From': {
                        'Email': 'nickstech707@gmail.com',
                        'Name': 'Spaces'
                    },
                    'To': [
                        {
                            'Email': to,
                            'Name': 'Recipient Name'
                        }
                    ],
                    'TemplateID': 6185052,  
                    'TemplateLanguage': True,
                    'Subject': 'Event Booking',
                    'Variables': {
                        'event_date': 'November 15th',
                        'message': 'Attending a trade show...'
                    }
                }
            ]
        }

        response = requests.post(
            mailjet_url,
            headers=headers,
            auth=(mailjet_api_key, mailjet_secret_key),
            json=email_data
        )

        if response.status_code == 200:
            return {"message": "Email sent"}, 200
        else:
            return {"message": "Failed to send email", "error": response.text}, response.status_code

api.add_resource(SendEmail, '/api/send-email')
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
api.add_resource(Events, '/api/events')
api.add_resource(EventByID, '/api/events/<int:event_id>/')

if __name__ == '__main__':
    app.run(port= 5555, debug=True)



