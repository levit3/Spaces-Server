#!/usr/bin/env python3
from flask import request, make_response, jsonify
from flask_restful import Resource

from config import app, db, api
from models import User, Review, Space, Payment


app.route('/')
def index():
    return "Welcome to Spaces."

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

class Spaces(Resource):
    def get(self):
      spaces = Space.query.all()
      space_data = [space.to_dict() for space in spaces]
      return make_response(jsonify(space_data), 200)
api.add_resource(Spaces, '/api/spaces>')

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

api.add_resource(Spaces, '/api/spaces/<int:space_id>')

