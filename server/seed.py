#!/usr/bin/env python3
from app import app
from models import User, Review, Space, Payment, Booking, UserRole, ReviewImage, SpaceImages
from faker import Faker
from config import db
from random import randint, choice, sample as rc
from datetime import datetime
from random import choice, randint
from faker import Faker
from sqlalchemy.orm import sessionmaker
fake = Faker()


if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

    #Create user data
        users =[]
        admin = User(name = 'admin', email = 'admin@admin.com', password = 'Admin@1234', role = UserRole.ADMIN, profile_picture = "https://i.pinimg.com/236x/6c/74/25/6c74255c82ac875ba9321bb44757407f.jpg")
        db.session.add(admin)
        db.session.commit()
        for _ in range(200):
            user = User(name=fake.name(), email=fake.email(), password=fake.password(length=10), role =rc([UserRole.USER, UserRole.TENANT], 1)[0], profile_picture="https://i.pinimg.com/236x/6c/74/25/6c74255c82ac875ba9321bb44757407f.jpg")
            users.append(user)
            db.session.add_all(users)
            db.session.commit()
        print("User data seeded successfully")

        #Create space data
        spaces = []
        tenants = User.query.filter_by(role='TENANT').all()
        for _ in range(50):
            tenant = choice(tenants)
            space = Space(title=fake.company(), description=fake.text(max_nb_chars=200), location=fake.city(), price_per_hour=randint(10, 300), status=rc(["available", "unavailable"], k=1)[0], tenant_id=tenant.id)
            spaces.append(space)
        db.session.add_all(spaces)
        db.session.commit()
        print("Space data seeded successfully")

        #Create booking data
        bookings = []
        for i in range(200):
            user_id = i
            space_id = choice(range(1, 50))
            start_date = fake.date_this_year()
            end_date = fake.date_between(start_date=start_date, end_date="+1y")

            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time())
            hours = (end_datetime - start_datetime).total_seconds() / 3600
            
            space = db.session.get(Space, space_id)
            total_price = hours * space.price_per_hour
            status = choice(["pending", "approved", "rejected"])
            created_at = fake.date_this_year()



            booking = Booking(
                user_id=user_id,
                space_id=space_id,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status=status,
                created_at=created_at
            )
            bookings.append(booking)
        db.session.add_all(bookings)
        db.session.commit()
        print("Booking data seeded successfully")

        #Create payment data
        payments = []
        for _ in range(200):
            booking_id = choice(range(1, 100))
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
            payments.append(payment)
        db.session.add_all(payments)
        db.session.commit()
        print("Payment data seeded successfully")

        #Create reviews data
        reviews =[]
        for _ in range(200):
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
                date=created_at
            )
            reviews.append(review)
        db.session.add_all(reviews)
        db.session.commit()
        print("Review data seeded successfully")


