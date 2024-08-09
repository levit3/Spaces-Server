#!/usr/bin/env python3
from flask import Flask, request, make_response, session, jsonify, redirect, flash
from flask_restful import Resource
import cloudinary
import jwt
import requests
from functools import wraps
from datetime import datetime, timedelta
from config import app, db, api, bcrypt
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
    def get(self, user_id):
    # def get(self, user_id, current_user):
        # if current_user.id != user_id:
        #     return jsonify({'message': 'Unauthorized'}), 403
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
        reviews = Review.query.all()
        return [review.to_dict() for review in reviews]
    
    # @token_required  
    def post(self):
        data = request.form
        images = request.files.getlist('images')

        try:
            review = Review(comment=data['comment'], rating=data['rating'], user_id=data['user_id'], space_id=data['space_id'])
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
    
class PaymentCancel(Resource):
    def get(self, payment_id):
        payment = Payment.query.get(payment_id)
        payment.status = 'cancelled'
        db.session.commit()
        return redirect("http://localhost:3000/payment", 302)
    
class PayPalExecutePayment(Resource):
    # @token_required
    def get(self, payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            return {"error": "Payment not found"}, 404

        paypal_payment_id = request.args.get('paymentId')
        payer_id = request.args.get('PayerID')

        paypal_payment = paypalrestsdk.Payment.find(paypal_payment_id)
        if paypal_payment.execute({"payer_id": payer_id}):
            payment.status = 'completed'
            db.session.commit()
            return {"message": "Payment completed successfully"}, 200
        else:
            payment.status = 'failed'
            db.session.commit()
            return {"error": "Payment execution failed"}, 400
        
class MpesaCallback(Resource):
    # @token_required
    def post(self, payment_id):
        data = request.get_json()
        payment = Payment.query.get(payment_id)
        if not payment:
            return {"error": "Payment not found"}, 404

        result_code = data.get('ResultCode')
        if result_code == '0':
            payment.status = 'completed'
        else:
            payment.status = 'failed'

        payment.mpesa_receipt_number = data.get('MpesaReceiptNumber', '')
        db.session.commit()

        return {"ResultCode": "0", "ResultDesc": "Success"}, 200

class Spaces(Resource):
    def get(self):
        spaces = Space.query.all()
        space_data = [space.to_dict() for space in spaces]
        return make_response(jsonify(space_data), 200)
    
    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        location = data.get('location')
        price_per_hour = data.get('price_per_hour')
        status = data.get('status')
        category = data.get('category')  

        space = Space(
            title=title,
            description=description,
            location=location,
            price_per_hour=price_per_hour,
            status=status,
            category=category  
        )
        db.session.add(space)
        db.session.commit()
        return space.to_dict(), 201
class SpaceByID(Resource):
    def get(self, space_id):
        space = Space.query.get(space_id)
        if space is None:
            return {"message": "Space not found"}, 404
        return space.to_dict(), 200

    def put(self, space_id):
        space = Space.query.get(space_id)
        if space is None:
            return {"message": "Space not found"}, 404
        data = request.get_json()
        for key, value in data.items():
            setattr(space, key, value)
        db.session.commit()
        return space.to_dict(), 200

    def delete(self, space_id):
        space = Space.query.get(space_id)
        if space is None:
            return {"message": "Space not found"}, 404
        db.session.delete(space)
        db.session.commit()
        return {"message": "Space deleted successfully"}, 200

    def patch(self, space_id):
        space = Space.query.get(space_id)
        if space is None:
            return {"message": "Space not found"}, 404
        data = request.get_json()
        for key, value in data.items():
            setattr(space, key, value)
        db.session.commit()
        return space.to_dict(), 200   
    
class Signup(Resource):
    def post(self):
        request_json = request.get_json()
        username = request_json.get('username')
        email = request_json.get('email')
        password = request_json.get('password')
        confirm_password = request_json.get('confirm_password')

        
        if password != confirm_password:
            return {'error': 'Passwords do not match'}, 400

        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'error': 'Email already in use'}, 400

        
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        new_user = User(username=username, email=email, password=password_hash)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

        token = jwt.encode({
            'id': new_user.id,
            'expiration': str(datetime.utcnow() + timedelta(days=5))
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return make_response({'user': new_user.to_dict(), 'token': token}, 201)
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
        

api.add_resource(MpesaCallback, '/api/callback/<int:payment_id>/')
api.add_resource(PaymentSuccess, '/api/payment_success/<int:payment_id>')
api.add_resource(PaymentCancel, '/api/payment_cancel/<int:payment_id>')
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
api.add_resource(Signup, '/api/signup')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(Events, '/api/events')
api.add_resource(EventByID, '/api/events/<int:event_id>/')

if __name__ == '__main__':
    app.run(port= 5555, debug=True)


