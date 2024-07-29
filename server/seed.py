#!/usr/bin/env python3
from app import app
from models import User, Review, Space, Payment, Booking
from faker import Faker
from config import db
from random import randint, choice, sample as rc
from datetime import datetime
from random import choice, randint
from faker import Faker
from sqlalchemy.orm import sessionmaker
fake = Faker()


if __name__ == '__main__':
    with app.app_context():
      pass

#Create user data
for _ in range(100):
    user = User(name=fake.name(), email=fake.email(), password=fake.password(length=10), role =rc(["user", "tenant"]), profile_picture="")
    db.session.add(user)
    db.session.commit()

#Create space data
for _ in range(50):
    space = Space(title=fake.company(), description=fake.text(max_nb_chars=200), location=fake.city(), price_per_hour=randint(10, 300), status=rc(["available", "unavailable"]), image_url=fake.image_url(), tenant_id=choice(range(1, 11)))
    db.session.add(space)
    db.session.commit()

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'))
    booking_id = db.Column(db.Integer,nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    updated_at = db.Column(db.Date, nullable=False)
    
   
#Create booking data
for _ in range(1000):
    user_id = choice(range(1, 100))
    space_id = choice(range(1, 50))
    booking_id = randint(1000, 9999)
    start_date = fake.date_this_year()
    end_date = fake.date_between(start_date=start_date, end_date="+1y")
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    hours = (end_datetime - start_datetime).total_seconds() / 3600
    space = db.session.query(Space).get(space_id)
    total_price = hours * space.price_per_hour
    status = choice(["pending", "approved", "rejected"])
    created_at = fake.date_this_year()

    booking = Booking(
        user_id=user_id,
        space_id=space_id,
        booking_id=booking_id,
        start_date=start_date,
        end_date=end_date,
        total_price=total_price,
        status=status,
        created_at=created_at
    )

    db.session.add(booking)

db.session.commit()


#Create payment data
for _ in range(500):
    booking_id = choice(range(1, 1000))
    amount = randint(10, 1000)
    payment_method = choice(["card", "paypal", "cash"])
    payment_status = choice(["pending", "paid", "failed"])
    created_at = fake.date_this_year()

    payment = Payment(
        booking_id=booking_id,
        amount=amount,
        payment_method=payment_method,
        payment_status=payment_status,
        created_at=created_at
    )

    db.session.add(payment)
    db.session.commit()


#Create reviews data
for _ in range(2000):
      user_id = choice(range(1, 100))
      space_id = choice(range(1, 50))
      rating = randint(1, 5)
      comment = fake.text(max_nb_chars=200)
      created_at = fake.date_this_year()

      review = Review(
          user_id=user_id,
          space_id=space_id,
          rating=rating,
          comment=comment,
          created_at=created_at
      )

      db.session.add(review)
      db.session.commit()
