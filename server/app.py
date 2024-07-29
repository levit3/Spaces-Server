#!/usr/bin/env python3
from flask import request, make_response
from flask_restful import Resource

from config import app, db, api
from models import User, Review, Space, Payment


app.route('/')
def index():
    return "Welcome to Spaces."


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
    



    
api.add_resource(Payments, '/api/payments/<int:payment_id>')