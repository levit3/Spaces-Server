#!/usr/bin/env python3
from flask import request, make_response
from flask_restful import Resource

from config import app, db, api
from models import User, Review, Space, Payment


app.route('/')
def index():
    return "Welcome to Spaces."
