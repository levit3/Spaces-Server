#!/usr/bin/env python3
from app import app
from models import User, Review, Space, Payment, Booking, UserRole, ReviewImage, SpaceImages, Event
from faker import Faker
from config import db
from random import randint, choice, sample as rc
from datetime import datetime, date
import logging

logging.getLogger('faker').setLevel(logging.WARNING)

fake = Faker()

def generate_unique_email(existing_emails):
    email = fake.email()
    while email in existing_emails:
        email = fake.email()
    existing_emails.add(email)
    return email

def seed_users():
    existing_emails = set()
    roles = [UserRole.USER, UserRole.TENANT]
    num_users = 10  # Number of users you want to create

    for _ in range(num_users):
        email = generate_unique_email(existing_emails)
        user = User(
            name=fake.name(),
            email=email,
            password=fake.password(length=10),
            role=rc(roles, 1)[0],
            profile_picture="https://i.pinimg.com/236x/6c/74/25/6c74255c82ac875ba9321bb44757407f.jpg"
        )
        db.session.add(user)

    db.session.commit()

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        # Create user data
        admin = User(name='admin', email='admin@admin.com', password='Admin@1234', role=UserRole.ADMIN, profile_picture="https://i.pinimg.com/236x/6c/74/25/6c74255c82ac875ba9321bb44757407f.jpg")
        db.session.add(admin)
        db.session.commit()

        users = []
        for _ in range(200):
            user = User(
                name=fake.name(),
                email=generate_unique_email(set([user.email for user in users])),
                password=fake.password(length=10),
                role=rc([UserRole.USER, UserRole.TENANT], 1)[0],
                profile_picture="https://i.pinimg.com/236x/6c/74/25/6c74255c82ac875ba9321bb44757407f.jpg"
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()
        print(f"User data seeded successfully. Total users: {len(users)}")

        # Create space data
        spaces = []
        tenants = User.query.filter_by(role=UserRole.TENANT).all()
        for _ in range(10):
            tenant = choice(tenants)
            space = Space(
                title=fake.company(),
                description=fake.text(max_nb_chars=200),
                location=fake.city(),
                price_per_hour=randint(10, 300),
                status=rc(["available", "unavailable"], k=1)[0],
                capacity=randint(50, 1000),
                tenant_id=tenant.id
            )
            spaces.append(space)
        db.session.add_all(spaces)
        db.session.commit()
        print(f"Space data seeded successfully. Total spaces: {len(spaces)}")

        #Create space_images data
        spaces = Space.query.all()       
        space_images = [
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDukxrvEf8vKC_0xErzjglzDy_AgasRMRxUw&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRh_FpfaZod6mxUYoIs0Sxkk6oEAgSRk0om6g&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBB2tiLXFYmC95eCyn5NstzNq_tD3ZwpXJ2A&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHTEY9evlMcvo_5pKvy-MJzzBWHyC89MNghA&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1aSCC1X7aXolYXV0iXd8CaogwyXpVE6et0g&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6iTXYRxbZxeRnaUXBPXbTXanVjP95blQWFw&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZusJwjgAN0dVvxBXPPbUsCEdXWAjBSy3qJQ&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8tPlYOSRYh8qvyPwCAVbuyLQUva1MwTKJEw&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTY0yOkusqNbOtWlUjoMFehPBwyV-I1rsnhB-mgjJGxKkAw9j1o8kxSnhly1L6dv2JRIVI&usqp=CAU",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVVit_Hr3g8K0mL1MuH0ahWMm1A1C940OfQPOvqH6Dy5gb8lhw07WUgRjREoG9fmRUXUI&usqp=CAU",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmKXW2QnAthetZOnCsgCSEj3G-mYyqOAQgSw&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQKR9ynFUDx_ICY7nV_bscBDhDnqJodQqA0XA&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBD6jiI1oe9z3C4YijGbXYNxwBdNtRdlgQag&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbKd8NxpAEvPN-UAMjOQyhOZAduLDWnDLzlqv5LzYCPOWa5WAPEaYjw-cFA8CBlDPwj4Q&usqp=CAU",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3WwmGruc4JziZYLJuUXkdvX1PwSr0KSVfm6hdL12ijrNyAuZEAMwSms37lnrfl0-F2b4&usqp=CAU",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7m5juDWYDnOJLfqCwc8nn-XmIHPnW5T3Dmw&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAtcK5JyZE3ZLySd0ZYUIvCLOhVAEWz1Pj3Q&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7hbsKj0yw_oqVeawYltDrePcP4xDsxSJpvA&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoQylMy25hHVJt90iMNP6qw3Bfms6_cHhgMQ&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQl1rrhGmdZEOSI4fhpxeCgeiVtOiANlfAuzLqYUSD_Ji1njx0KXHO5bBKAO71bZgWasRM&usqp=CAU",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1Jo2T-CyjMAfCHu19Y9zVX3GyQkY2r7vlrXq_4sPtFReP8xA4Apwrso5sjNBFTn5kVf8&usqp=CAU",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdVVX4ZnbNCVSLCmMVadzFxO_bEiYMnTtxtT22O0DAoUGBg1RdXXRcPGMsBwEs-xXD7Sg&usqp=CAU",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFtxq3Dy8eTnKAa1n3x23xSBlunveXGFgr_Q&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBV-K6rLOEcY7vp-AMkaVHf_5FR0-eE2K62g&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZPDAKmTGpGdQFbKFKq9gfkrydb5if--S5fQ&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKHpUQnO1YkNxwuGnN05IO_SSzrdNzuz-9RA&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSV7jKikBan_q-YhzqZIu5cRS9sxZy5TccRHQ&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3ELftifm2xXmsEotUw9qtmYBuW53NaL2G4w&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTn9anCOds0aZJDhL3cUsEOqJ6urRdT_0Mjg&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9OM3BvloKFXYYCvqZKmnhe5q4bvgnX3LvEg&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFVQWZQoz2BOYnIeQGQ4rum89Jgz01-vebKg&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6M0WKaaliIJb3zRFEkbJM_dQIlbVlyY217A&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQklTyVbamFbUBQWqDHgO-djovvLBWV2zRwzA&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwbGLE8538lHL5_x1u1AwGOOwDGrTKwsIwnQ&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQKcxNxWcgMOJTSSzGchzP3vFq-8ydhplgFtw&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgGaCFLbB1hRQnbXnB9JOOO4vvP_ehRbqehw&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRinBt-dGanCh9cy2c5gMHIMZpjNkrguT7M4w&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8RS4N3GTTNu_hE_O0czavuCseylFU9IQoQg&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjD6Zjx06b5OIfGrj1XQ7hRqg4UKq3Rc2QqQ&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGeI6be1l5nFx752kcU8y6jxtmsGugYvC7Cw&s",
                    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqxrzw3sRFwoMy2teoaO_oedw6-EbasiLEbQ&s",
                    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsv5BghQypAA9vL-F_dueyDaJmYiYCsfyZUA&s",
                    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0q1-ZXX1ueiy5mmfD8HkhEt6Sc_jNf4xeNg&s",
                    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT27H5Kc3MuLwzQMvZdT76_yeiEgabghpwpSw&s",
                    
                     ]
        for space in spaces:
            assigned_images = rc(space_images, 4)  
            for img_url in assigned_images:
                space_image = SpaceImages(
                    space_id=space.id,
                    image_url=img_url
                )
                db.session.add(space_image)
                space_images.remove(img_url)  

        db.session.commit()
        print(f"Space image data seeded successfully.")

        # Create booking data
        bookings = []
        users = User.query.filter_by(role=UserRole.USER).all()
        for _ in range(200):
            user_id = choice(users).id
            space_id = choice(range(1, 10))
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
        print(f"Booking data seeded successfully. Total bookings: {len(bookings)}")

        # Create payment data
        payments = []
        for i in range(200):
            payment = Payment(
                booking_id=i + 1,
                amount=randint(10, 1000),
                payment_method=choice(["card", "paypal", "cash"]),
                payment_status=choice(["pending", "paid", "failed"]),
                created_at=fake.date_this_year()
            )
            payments.append(payment)
        db.session.add_all(payments)
        db.session.commit()
        print(f"Payment data seeded successfully. Total payments: {len(payments)}")

        # Create reviews data
        reviews = []
        users = User.query.filter_by(role='USER').all()
        for _ in range(200):
            user_id = choice(users).id
            user = User.query.filter_by(id=user_id).first()
            bookings = user.bookings
            if bookings:
                booking = choice(bookings)
                space_id = booking.space_id
                review = Review(
                    user_id=user_id,
                    space_id=space_id,
                    rating=randint(1, 5),
                    comment=fake.text(max_nb_chars=200),
                    date=fake.date_this_year()
                )
                reviews.append(review)
        db.session.add_all(reviews)
        db.session.commit()
        print(f"Review data seeded successfully. Total reviews: {len(reviews)}")


        # Create events
        events = []

        # Sample users and spaces
        users = User.query.all()
        spaces = Space.query.filter_by(status='unavailable').all()

        # Manually defining 50 sample events
        sample_events = [
            {
                "title": "Summer Networking Event",
                "description": "Join us for a fun networking event with industry professionals.",
                "date": date(2024, 8, 19),  # Adjusted to 19/08/2024
                "image_url": "https://example.com/images/networking.jpg"
            },
            {
                "title": "Tech Innovation Conference",
                "description": "A conference discussing the latest trends in technology and innovation.",
                "date": date(2024, 8, 25),  # Adjusted to 25/08/2024
                "image_url": "https://example.com/images/tech_conference.jpg"
            },
            {
                "title": "Art and Design Expo",
                "description": "Explore the world of art and design at our annual expo.",
                "date": date(2024, 9, 5),  # Adjusted to 05/09/2024
                "image_url": "https://example.com/images/art_expo.jpg"
            },
            {
                "title": "Business Growth Summit",
                "description": "Learn strategies for growing your business at our annual summit.",
                "date": date(2024, 9, 12),  # Adjusted to 12/09/2024
                "image_url": "https://example.com/images/business_summit.jpg"
            },
            {
                "title": "Health and Wellness Fair",
                "description": "A fair dedicated to promoting health and wellness in the community.",
                "date": date(2024, 11, 15),
                "image_url": "https://example.com/images/wellness_fair.jpg"
            },
            {
                "title": "Music Festival Extravaganza",
                "description": "Experience live music from top artists at our annual festival.",
                "date": date(2024, 10, 12),
                "image_url": "https://example.com/images/music_festival.jpg"
            },
            {
                "title": "Culinary Arts Showcase",
                "description": "Taste and learn from the best chefs in the culinary world.",
                "date": date(2024, 9, 5),
                "image_url": "https://example.com/images/culinary_arts.jpg"
            },
            {
                "title": "Startup Pitch Night",
                "description": "Watch startups pitch their innovative ideas to potential investors.",
                "date": date(2024, 9, 18),
                "image_url": "https://example.com/images/pitch_night.jpg"
            },
            {
                "title": "Fashion Week Gala",
                "description": "Celebrate the latest trends in fashion with top designers.",
                "date": date(2024, 10, 2),
                "image_url": "https://example.com/images/fashion_week.jpg"
            },
            {
                "title": "Environmental Awareness Conference",
                "description": "Discuss the challenges and solutions for environmental sustainability.",
                "date": date(2024, 11, 10),
                "image_url": "https://example.com/images/environmental_conference.jpg"
            },
            {
                "title": "Film Screening and Discussion",
                "description": "Join us for a film screening followed by a panel discussion.",
                "date": date(2024, 12, 22),
                "image_url": "https://example.com/images/film_screening.jpg"
            },
            {
                "title": "Charity Fundraising Gala",
                "description": "Support a great cause by attending our charity fundraising gala.",
                "date": date(2024, 9, 25),
                "image_url": "https://example.com/images/charity_gala.jpg"
            },
            {
                "title": "Outdoor Adventure Expo",
                "description": "Explore outdoor gear and activities at our adventure expo.",
                "date": date(2024, 9, 7),
                "image_url": "https://example.com/images/adventure_expo.jpg"
            },
            {
                "title": "Photography Workshop",
                "description": "Improve your photography skills with expert guidance.",
                "date": date(2024, 10, 12),
                "image_url": "https://example.com/images/photography_workshop.jpg"
            },
            {
                "title": "Book Fair and Author Meet",
                "description": "Meet your favorite authors and discover new books at our fair.",
                "date": date(2024, 11, 2),
                "image_url": "https://example.com/images/book_fair.jpg"
            },
            {
                "title": "Startup Expo",
                "description": "Showcase your startup and connect with investors and customers.",
                "date": date(2024, 9, 18),
                "image_url": "https://example.com/images/startup_expo.jpg"
            },
            {
                "title": "Cultural Festival",
                "description": "Celebrate diverse cultures with music, dance, and food.",
                "date": date(2024, 9, 25),
                "image_url": "https://example.com/images/cultural_festival.jpg"
            },
            {
                "title": "Tech Bootcamp",
                "description": "Learn the latest technology skills in an intensive bootcamp.",
                "date": date(2024, 10, 5),
                "image_url": "https://example.com/images/tech_bootcamp.jpg"
            },
            {
                "title": "Science Symposium",
                "description": "Discuss groundbreaking research and discoveries in science.",
                "date": date(2024, 11, 20),
                "image_url": "https://example.com/images/science_symposium.jpg"
            },
            {
                "title": "Meditation and Mindfulness Retreat",
                "description": "Find peace and relaxation at our meditation retreat.",
                "date": date(2024, 9, 30),
                "image_url": "https://example.com/images/meditation_retreat.jpg"
            },
            {
                "title": "Fitness Challenge Event",
                "description": "Participate in our fitness challenge and push your limits.",
                "date": date(2024, 9, 15),
                "image_url": "https://example.com/images/fitness_challenge.jpg"
            },
            {
                "title": "Wine Tasting Event",
                "description": "Sample a variety of wines at our exclusive tasting event.",
                "date": date(2024, 9, 10),
                "image_url": "https://example.com/images/wine_tasting.jpg"
            },
            {
                "title": "Craft and Handmade Fair",
                "description": "Discover unique handmade crafts and goods at our fair.",
                "date": date(2024, 10, 8),
                "image_url": "https://example.com/images/craft_fair.jpg"
            },
            {
                "title": "Outdoor Movie Night",
                "description": "Enjoy a classic movie under the stars at our outdoor screening.",
                "date": date(2024, 11, 3),
                "image_url": "https://example.com/images/movie_night.jpg"
            },
            {
                "title": "Dance Workshop",
                "description": "Learn new dance moves from professional instructors.",
                "date": date(2024, 9, 14),
                "image_url": "https://example.com/images/dance_workshop.jpg"
            },
            {
                "title": "Yoga and Wellness Retreat",
                "description": "Rejuvenate your body and mind at our yoga retreat.",
                "date": date(2024, 8, 22),
                "image_url": "https://example.com/images/yoga_retreat.jpg"
            },
            {
                "title": "Sustainability Workshop",
                "description": "Learn how to live a more sustainable lifestyle.",
                "date": date(2024, 9, 29),
                "image_url": "https://example.com/images/sustainability_workshop.jpg"
            },
            {
                "title": "Startup Networking Night",
                "description": "Connect with fellow entrepreneurs at our networking night.",
                "date": date(2024, 10, 15),
                "image_url": "https://example.com/images/networking_night.jpg"
            },
            {
                "title": "Food Truck Festival",
                "description": "Sample delicious food from the best food trucks in town.",
                "date": date(2024, 11, 12),
                "image_url": "https://example.com/images/food_truck_festival.jpg"
            },
            {
                "title": "Digital Marketing Conference",
                "description": "Stay ahead of the trends in digital marketing.",
                "date": date(2024, 10, 26),
                "image_url": "https://example.com/images/marketing_conference.jpg"
            },
            {
                "title": "Gardening Expo",
                "description": "Learn tips and tricks for your garden at our expo.",
                "date": date(2024, 8, 28),
                "image_url": "https://example.com/images/gardening_expo.jpg"
            },
            {
                "title": "Outdoor Yoga Session",
                "description": "Join us for a refreshing outdoor yoga session.",
                "date": date(2024, 9, 12),
                "image_url": "https://example.com/images/outdoor_yoga.jpg"
            },
            {
                "title": "Artisan Market",
                "description": "Shop unique handmade goods at our artisan market.",
                "date": date(2024, 10, 20),
                "image_url": "https://example.com/images/artisan_market.jpg"
            },
            {
                "title": "Coding Hackathon",
                "description": "Test your coding skills in our 24-hour hackathon.",
                "date": date(2024, 11, 7),
                "image_url": "https://example.com/images/hackathon.jpg"
            },
            {
                "title": "Wine and Cheese Evening",
                "description": "Enjoy an evening of wine and cheese pairing.",
                "date": date(2024, 9, 18),
                "image_url": "https://example.com/images/wine_cheese.jpg"
            },
            {
                "title": "Baking Workshop",
                "description": "Learn how to bake delicious treats from professional bakers.",
                "date": date(2024, 9, 12),
                "image_url": "https://example.com/images/baking_workshop.jpg"
            },
            {
                "title": "Sustainable Fashion Show",
                "description": "Explore the latest in sustainable fashion at our show.",
                "date": date(2024, 9, 3),
                "image_url": "https://example.com/images/fashion_show.jpg"
            },
            {
                "title": "Film Festival",
                "description": "Watch award-winning films at our annual film festival.",
                "date": date(2024, 10, 1),
                "image_url": "https://example.com/images/film_festival.jpg"
            },
            {
                "title": "Tech Talks Seminar",
                "description": "Listen to experts discuss the latest in technology.",
                "date": date(2024, 11, 17),
                "image_url": "https://example.com/images/tech_talks.jpg"
            },
            {
                "title": "Craft Beer Tasting",
                "description": "Sample a variety of craft beers from local breweries.",
                "date": date(2024, 10, 20),
                "image_url": "https://example.com/images/beer_tasting.jpg"
            },
            {
                "title": "Culinary Experience",
                "description": "Enjoy a multi-course meal prepared by top chefs.",
                "date": date(2024, 8, 30),
                "image_url": "https://example.com/images/culinary_experience.jpg"
            },
            {
                "title": "Startup Founders Meetup",
                "description": "Meet and learn from successful startup founders.",
                "date": date(2024, 9, 9),
                "image_url": "https://example.com/images/founders_meetup.jpg"
            },
            {
                "title": "Holiday Market",
                "description": "Shop for unique holiday gifts at our holiday market.",
                "date": date(2024, 12, 5),
                "image_url": "https://example.com/images/holiday_market.jpg"
            },
            {
                "title": "Blockchain Seminar",
                "description": "Learn about the impact of blockchain technology.",
                "date": date(2024, 10, 17),
                "image_url": "https://example.com/images/blockchain_seminar.jpg"
            },
            {
                "title": "Outdoor Art Fair",
                "description": "Discover local artists and their work at our outdoor fair.",
                "date": date(2024, 11, 21),
                "image_url": "https://example.com/images/art_fair.jpg"
            },
            {
                "title": "Cider Tasting Event",
                "description": "Taste a variety of ciders at our tasting event.",
                "date": date(2024, 9, 27),
                "image_url": "https://example.com/images/cider_tasting.jpg"
            },
            {
                "title": "Literary Salon",
                "description": "Join authors for a discussion on literature and writing.",
                "date": date(2024, 9, 14),
                "image_url": "https://example.com/images/literary_salon.jpg"
            },
            {
                "title": "Startup Workshop",
                "description": "Learn how to launch and scale your startup.",
                "date": date(2024, 9, 24),
                "image_url": "https://example.com/images/startup_workshop.jpg"
            }
        ]

        # Repeat and adjust for 50 events
        for i in range(50):
            if spaces and users:
                space = spaces[i % len(spaces)]
                user = users[i % len(users)]
                            
                event_data = sample_events[i % len(sample_events)]
                event = Event(
                    title=f"{event_data['title']} - Edition {i+1}",
                    description=event_data['description'],
                    date=event_data['date'],
                    organizer_id=user.id,
                    space_id=space.id,
                    image_url=event_data['image_url']
                )
                events.append(event)

        db.session.add_all(events)
        db.session.commit()
        print(f"Events seeded successfully.")