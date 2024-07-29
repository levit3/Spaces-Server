#!/usr/bin/env python3
from app import app
from models import User, Review, Space, Payment
from faker import Faker
fake = Faker()


if __name__ == '__main__':
    with app.app_context():
      pass