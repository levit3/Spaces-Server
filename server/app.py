#!/usr/bin/env python3
from flask import Flask, request, make_response, session, jsonify, redirect, flash
from flask_restful import Resource
import cloudinary
import jwt

import requests
from functools import wraps
from datetime import datetime, timedelta
from config import app, db, api
from models import User, Review, Space, Payment, Booking, ReviewImage, Event
import cloudinary.uploader
import cloudinary.api
from requests.auth import HTTPBasicAuth
import base64
import paypalrestsdk
import logging
from werkzeug.exceptions import BadRequest
import re
from flask import Flask
# app = Flask(__name__)
# api=Api(app)


logging.basicConfig(level=logging.DEBUG)

# M-Pesa configuration
consumer_key = "iUAZGP5jVKh3aGWbl1BfQcEiax5UbhApLFhvh6Q0puqMbMpo"
consumer_secret = "f8VEXQiNQ5GuseSZQVM1sdsQS2mEuJn4D62MAhAYkqDzRjhLXD5n6dNjk68uRMpC"
shortcode = "174379"
passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
callback_url = "https://mydomain.com/path"

# M-Pesa validation
def get_oauth_token():
    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode('utf-8')
    response = requests.get(
        'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
        headers={'Authorization': f'Basic {auth}'}
    )
    response.raise_for_status()
    return response.json()['access_token']

# Phone number validation
def validate_and_format_phone_number(phone_number):
    phone_number = re.sub(r'\D', '', phone_number)
    if not phone_number.startswith('254'):
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        else:
            phone_number = '254' + phone_number
    return phone_number

# PayPal configuration
paypalrestsdk.configure({
  "mode": "live",
  "client_id": "Acm84K466flWgwo-jGejv8-RfoKFHNh8T5lDevWHTCxUiZirnXzn3DznjQTOGbjCkIO1fuMhYZjQj4To",
  "client_secret": "EPZX93R4UNJLPneP89oB3RaGipsNhCBNRvNRBfyv9V-YFbydUfseSZxz8CKiukfjbyftpFtU4SWfqCPj"
})

# Cloudinary configuration
cloudinary.config(
  cloud_name='dzqt3usfp',
  api_key='618183139173486',
  api_secret='6oUAsFqSzho3xOjxebi3SIUps9U'
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
        booking_arr = Booking.query.all()
        bookings = [booking.to_dict() for booking in booking_arr]
        return make_response(bookings, 200)
    
    def post(self):
        data = request.json
        booking = Booking(
            user_id=data['user_id'],
            space_id=data['space_id'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            total_price=data['total_price'],
            status=data['status'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
        db.session.add(booking)
        db.session.commit()
        return make_response(booking.to_dict(), 200)
        
class BookingByID(Resource):
    def get(self, booking_id):
        booking = Booking.query.filter_by(id=booking_id).first()
        return make_response(booking.to_dict(), 200)
    
    def put(self, booking_id):
        booking = Booking.query.get(booking_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(booking, key, value)
        db.session.commit()
        return make_response(booking.to_dict(), 200)

    def delete(self, booking_id):
        booking = Booking.query.get(booking_id)
        db.session.delete(booking)
        db.session.commit()
        return make_response(booking.to_dict(), 200)

    def patch(self, booking_id):
        booking = Booking.query.get(booking_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(booking, key, value)
        db.session.commit()
        return make_response(booking.to_dict(), 200)

class Users(Resource):
    def get(self):
        users = User.query.all()
        user = [user.to_dict() for user in users]
        return make_response(user)
    
class UserByID(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return make_response(user.to_dict())
    
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
    
    def patch(self, user_id):
        user = User.query.get(user_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user.to_dict()

class Reviews(Resource):
    def get(self):
        reviews = Review.query.all()
        return [review.to_dict() for review in reviews]
    
    def post(self):
        data = request.form
        images = request.files.getlist('images')

        try:
            review = Review(
                comment=data['comment'],
                rating=data['rating'],
                user_id=data['user_id'],
                space_id=data['space_id']
            )
            db.session.add(review)

            if images:
                for image in images:
                    upload_result = cloudinary.uploader.upload(image)
                    review_image = ReviewImage(image_url=upload_result['url'])
                    review.images.append(review_image)

            db.session.commit()
            return review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

class ReviewByID(Resource):
    def get(self, review_id):
        review = Review.query.get_or_404(review_id)
        return review.to_dict(), 200

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
class Spaces(Resource):
    class Spaces(Resource):
     def get(self):
        spaces = Space.query.all()
        space_data = [space.to_dict() for space in spaces]
        return make_response(space_data), 200
    
    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        location = data.get('location')
        price_per_hour = data.get('price_per_hour')
        status = data.get('status')
        tenant_id = 7 

        if not tenant_id:
            return make_response(jsonify({"error": "Tenant not added"}), 400)

        space = Space(
            title=title,
            description=description,
            location=location,
            price_per_hour=price_per_hour,
            status=status,
            tenant_id=tenant_id
        )
        db.session.add(space)
        db.session.commit()
        return make_response(jsonify(space.to_dict()), 201)

class SpaceByID(Resource):
    def get(self, space_id):
        space = Space.query.get(space_id)
        if not space:
            return make_response(jsonify({"error": "Space not found"}), 404)
        return space.to_dict(), 200

    def put(self, space_id):
        space = Space.query.get(space_id)
        if not space:
            return make_response(jsonify({"error": "Space not found"}), 404)
       
        for attr in request.json:
            setattr(space,attr,request.json[attr])
        db.session.add(space)
        db.session.commit()
        return make_response(space.to_dict()), 200

    def delete(self, space_id):
        space = Space.query.get(space_id)
        if not space:
            return make_response(jsonify({"error": "Space not found"}), 404)
        
        db.session.delete(space)
        db.session.commit()
        return make_response(jsonify(space.to_dict()), 200)

    def patch(self, space_id):
        space = Space.query.get(space_id)
        if not space:
            return make_response(jsonify({"error": "Space not found"}), 404)
        
        data = request.get_json()
        for key, value in data.items():
            setattr(space, key, value)
        db.session.commit()
        return make_response(jsonify(space.to_dict()), 200)
    
class Payments(Resource):
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
    def get(self, payment_id):
        payment = Payment.query.get(payment_id)
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

    def post(self, payment_id):
        payment = db.session.get(Payment, payment_id)
        if not payment:
            return {"error": "Payment not found"}, 404

        data = request.json
        token = get_oauth_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            headers=headers,
            json={
                "BusinessShortCode": shortcode,
                "Password": base64.b64encode(f"{shortcode}{passkey}{datetime.now().strftime('%Y%m%d%H%M%S')}".encode()).decode(),
                "Timestamp": datetime.now().strftime('%Y%m%d%H%M%S'),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": data['amount'],
                "PartyA": validate_and_format_phone_number(data['phone_number']),
                "PartyB": shortcode,
                "PhoneNumber": validate_and_format_phone_number(data['phone_number']),
                "CallBackURL": callback_url,
                "AccountReference": "SpacesForRent",
                "TransactionDesc": "Payment for booking"
            }
        )
        response.raise_for_status()
        return response.json()

api.add_resource(Bookings, '/bookings')
api.add_resource(BookingByID, '/bookings/<int:booking_id>')
api.add_resource(Users, '/api/users')
api.add_resource(UserByID, '/api/users/<int:user_id>')
api.add_resource(Reviews, '/reviews')
api.add_resource(ReviewByID, '/reviews/<int:review_id>')
api.add_resource(Payments, '/payments')
api.add_resource(PaymentByID, '/payments/<int:payment_id>')
api.add_resource(Spaces, '/api/spaces')
api.add_resource(SpaceByID, '/api/spaces/<int:space_id>/')


if __name__ == "__main__":
    app.run(debug=True,port=5555)
