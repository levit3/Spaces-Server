#!/usr/bin/env python3
from flask import Flask, request, make_response, session, jsonify, redirect, flash
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
from requests.auth import HTTPBasicAuth
import base64
import paypalrestsdk
from flask_cors import CORS
import requests
from datetime import datetime
import re
import logging


logging.basicConfig(level=logging.DEBUG)

#M-pesa configuration
consumer_key = "iUAZGP5jVKh3aGWbl1BfQcEiax5UbhApLFhvh6Q0puqMbMpo"
consumer_secret = "f8VEXQiNQ5GuseSZQVM1sdsQS2mEuJn4D62MAhAYkqDzRjhLXD5n6dNjk68uRMpC"
shortcode = "174379"
passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
callback_url = "https://mydomain.com/path"
# callback_url = "http://127.0.0.1:5555/api/callback/<int:payment_id>/"

# M-pesa validation
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
    # @token_required
    def get(self, user_id, current_user):
        if current_user.id != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        user = User.query.filter_by(id = user_id).first()
        return make_response(user.to_dict(), 200)
    
    # @token_required      
    def put(self, user_id):
        user = User.query.get(user_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user.to_dict()

    # @token_required      
    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return user.to_dict()
    
    # @token_required      
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
    
    # @token_required
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

    # @token_required
    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted'}, 200
    
    # @token_required
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

    # @token_required  
    def put(self, payment_id):
        payment = Payment.query.get(payment_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(payment, key, value)
        db.session.commit()
        return payment.to_dict()

    # @token_required
    def delete(self, payment_id):
        payment = Payment.query.get(payment_id)
        db.session.delete(payment)
        db.session.commit()
        return payment.to_dict()
    
    # @token_required  
    def patch(self, payment_id):
        payment = Payment.query.get(payment_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(payment, key, value)
        db.session.commit()
        return payment.to_dict()

    # @token_required  
    def post(self, payment_id):
        payment = db.session.get(Payment, payment_id)
        if not payment:
            return {"error": "Payment not found"}, 404

        data = request.get_json()
        if not data:
            return {"error": "No JSON data provided"}, 400

        payment_method = data.get('payment_method')
        if not payment_method:
            return {"error": "Payment method is required"}, 400

        try:
            if payment_method == 'mpesa':
                return self.initiate_mpesa_payment(payment, data)
            elif payment_method == 'paypal':
                return self.initiate_paypal_payment(payment)
            else:
                return {"error": "Invalid payment method"}, 400
        except Exception as e:
            logging.error(f"Error processing payment: {str(e)}")
            return {"error": "An error occurred while processing the payment", "details": str(e)}, 500

    # @token_required  
    def initiate_mpesa_payment(self, payment, data):
        phone_number = data.get('phone_number')
        if not phone_number:
            return {"error": "Phone number is required"}, 400

        phone_number = validate_and_format_phone_number(phone_number)

        access_token = get_oauth_token()

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payload = {
            "BusinessShortCode": int(shortcode),
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            # "Amount": int(payment.amount),
            "Amount": int(1),
            "PartyA": int(phone_number),
            "PartyB": int(shortcode),
            "PhoneNumber": int(phone_number),
            "CallBackURL": callback_url,
            "AccountReference": f"Payment{payment.id}",
            "TransactionDesc": f"Payment for order {payment.id}"
        }

        logging.debug(f"Payload: {payload}")

        try:
            response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
                                     headers=headers,
                                     json=payload)
            response.raise_for_status()

            logging.debug(f"M-Pesa API Response: {response.text}")

            if response.status_code == 200:
                payment.status = 'pending'
                payment.payment_method = 'mpesa'
                db.session.commit()
                return response.json(), 200
            else:
                return {"error": "M-Pesa request failed", "details": response.text}, response.status_code
        except requests.exceptions.RequestException as e:
            logging.error(f"Error making request to M-Pesa API: {str(e)}")
            return {"error": "Failed to communicate with M-Pesa API", "details": str(e)}, 500
        
    # @token_required
    def initiate_paypal_payment(self, payment):
        paypal_payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": f"http://127.0.0.1:5555/api/payment_success/{payment.id}",
                "cancel_url": f"http://127.0.0.1:5555/api/payment_cancel/{payment.id}"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": f"Payment {payment.id}",
                        "sku": f"PAYMENT-{payment.id}",
                        "price": str(payment.amount),
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": str(payment.amount),
                    "currency": "USD"},
                "description": f"Payment for order {payment.id}"}]})

        if paypal_payment.create():
            payment.status = 'pending'
            payment.payment_method = 'paypal'
            payment.paypal_payment_id = paypal_payment.id
            db.session.commit()

            for link in paypal_payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return {"approval_url": approval_url}, 200
        else:
            return {"error": paypal_payment.error}, 400
        
class PaymentSuccess(Resource):
    def get(self, payment_id):
        payment = Payment.query.get(payment_id)
        payment.status = 'success'
        db.session.commit()
        return {"message": "Payment processed successfully."}, 200
