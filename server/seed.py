#!/usr/bin/env python3
from app import app
from models import User, Review, Space, Payment, Booking, ReviewImage, SpaceImages, UserRole
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
    #Create user data
        for _ in range(200):
            user = User(name=fake.name(), email=fake.email(), password=fake.password(length=10), role =rc([UserRole.USER, UserRole.TENANT], k=1)[0], profile_picture="https://i.pinimg.com/236x/6c/74/25/6c74255c82ac875ba9321bb44757407f.jpg")
            db.session.add(user)
            db.session.commit()
        print("User data seeding completed successfully")

        #Create space data
        for _ in range(50):
            space = Space(title=fake.company(), description=fake.text(max_nb_chars=200), location=fake.city(), price_per_hour=randint(10, 300), status=rc(["available", "unavailable"], k=1)[0], tenant_id=choice(range(1, 100)))
            db.session.add(space)
            db.session.commit()
        print("Space data seeded successfully")

        #Create booking data
        for _ in range(200):
            user_id = choice(range(1, 200))
            space_id = choice(range(1, 50))
            start_date = fake.date_this_year()
            end_date = fake.date_between(start_date=start_date, end_date="+1y")
            start_datetime = datetime.strptime(str(start_date), '%Y-%m-%d')
            end_datetime = datetime.strptime(str(end_date), '%Y-%m-%d')
            hours = (end_datetime - start_datetime).total_seconds() / 3600
            space = db.session.query(Space).get(space_id)
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

            db.session.add(booking)
            db.session.commit()
        print("Booking data seeded successfully")

        #Create payment data
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

            db.session.add(payment)
            db.session.commit()
        print("Payment data seeded successfully")

        #Create reviews data
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

            db.session.add(review)
            db.session.commit()
        print("Review data seeded successfully")


#Create review images data
for _ in range(2000):
    review_id = choice(range(1, 2000))
    image_url = fake.image_url()
    review_image = ReviewImage(
        review_id=review_id,
        image_url=image_url
    )
    db.session.add(review_image)
    db.session.commit()


print("Review images seeded successfully")
#Create space images data
for _ in range(50):
    space_id = choice(range(1, 50))
    image_url = fake.image_url()
    space_image = SpaceImages(
        space_id=space_id,
        image_url=image_url
    )
    db.session.add(space_image)
    db.session.commit()


print("Space images seeded successfully")
