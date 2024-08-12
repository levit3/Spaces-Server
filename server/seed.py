#!/usr/bin/env python3
from app import app
from models import User, Review, Space, Payment, Booking, UserRole, ReviewImage, SpaceImages, Event
from faker import Faker
from config import db
from random import randint, choice, sample as rc
from datetime import datetime
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
        space_list = [
    {
        "title": "Executive Conference Room",
        "description": "A spacious room designed for high-profile board meetings, featuring state-of-the-art conferencing equipment, ergonomic seating, and a stunning city view. Ideal for teams that require a professional and sophisticated environment.",
        "location": "New York",
        "price_per_hour": 200,
        "status": "available"
    },
    {
        "title": "Cozy Private Office",
        "description": "A comfortable and quiet private office space perfect for solo work or small teams. Equipped with modern office furniture, high-speed internet, and a peaceful atmosphere, making it ideal for productivity.",
        "location": "Los Angeles",
        "price_per_hour": 150,
        "status": "unavailable"
    },
    {
        "title": "Grand Event Hall",
        "description": "A large, elegant event hall suitable for weddings, corporate events, and other large gatherings. Features include a grand stage, advanced lighting, and sound systems, as well as ample seating and catering facilities.",
        "location": "Chicago",
        "price_per_hour": 300,
        "status": "available"
    },
    {
        "title": "Modern Training Room",
        "description": "This room is designed for corporate training sessions and seminars. It comes equipped with modern audio-visual equipment, comfortable seating, and flexible layouts to accommodate various training needs.",
        "location": "Houston",
        "price_per_hour": 250,
        "status": "available"
    },
    {
        "title": "Creative Studio",
        "description": "A versatile studio space perfect for photoshoots, video production, and creative projects. The space offers excellent natural lighting, a variety of backdrops, and high-quality soundproofing.",
        "location": "San Francisco",
        "price_per_hour": 180,
        "status": "unavailable"
    },
    {
        "title": "Luxury Meeting Room",
        "description": "An upscale meeting room designed for executive meetings. The room features high-end furniture, advanced conferencing technology, and a luxurious ambiance that ensures a professional and comfortable environment.",
        "location": "Miami",
        "price_per_hour": 220,
        "status": "available"
    },
    {
        "title": "Shared Workspace",
        "description": "A flexible and collaborative co-working space that fosters creativity and networking. The space includes open desks, private booths, and breakout areas, all equipped with high-speed internet and modern amenities.",
        "location": "Austin",
        "price_per_hour": 80,
        "status": "available"
    },
    {
        "title": "Private Workshop",
        "description": "This space is ideal for small group workshops, offering a quiet and focused environment. The workshop space includes flexible seating arrangements, presentation tools, and whiteboards.",
        "location": "Denver",
        "price_per_hour": 130,
        "status": "unavailable"
    },
    {
        "title": "Urban Loft Office",
        "description": "A modern office space with a unique loft design, featuring high ceilings, large windows, and an open-plan layout. Ideal for creative teams looking for an inspiring work environment.",
        "location": "Seattle",
        "price_per_hour": 170,
        "status": "available"
    },
    {
        "title": "Tech Hub Conference Room",
        "description": "A state-of-the-art conference room located in the heart of the tech district. Equipped with the latest in conferencing technology, including video conferencing, large displays, and smart whiteboards.",
        "location": "San Jose",
        "price_per_hour": 210,
        "status": "available"
    },
    {
        "title": "Downtown Event Space",
        "description": "A centrally located event space perfect for corporate functions, social gatherings, and other events. The space features a modern design, flexible seating, and full catering services.",
        "location": "Boston",
        "price_per_hour": 250,
        "status": "unavailable"
    },
    {
        "title": "Creative Co-Working Space",
        "description": "A vibrant co-working environment designed for freelancers, startups, and small businesses. The space offers a mix of private offices, open desks, and collaborative areas, all within a creative and inspiring setting.",
        "location": "Portland",
        "price_per_hour": 90,
        "status": "available"
    },
    {
        "title": "Beachside Conference Room",
        "description": "A unique conference room offering breathtaking ocean views. This space is ideal for meetings that require a calm and inspiring environment, complete with modern conferencing technology and comfortable seating.",
        "location": "San Diego",
        "price_per_hour": 190,
        "status": "available"
    },
    {
        "title": "Rustic Barn Event Venue",
        "description": "A charming venue located in a rustic barn, perfect for weddings, social events, and intimate gatherings. The space features exposed wooden beams, a spacious layout, and beautiful countryside views.",
        "location": "Nashville",
        "price_per_hour": 230,
        "status": "unavailable"
    },
    {
        "title": "Luxury Private Office",
        "description": "An exclusive private office with premium amenities, including high-speed internet, luxury furnishings, and a private meeting area. Perfect for professionals who require a high-end workspace.",
        "location": "Dallas",
        "price_per_hour": 260,
        "status": "available"
    },
    {
        "title": "Modern Conference Suite",
        "description": "A suite of conference rooms designed for large meetings, workshops, and breakout sessions. The space includes modern technology, flexible seating arrangements, and catering options.",
        "location": "Atlanta",
        "price_per_hour": 300,
        "status": "available"
    },
    {
        "title": "Historic Meeting Room",
        "description": "A meeting room with a classic design, featuring antique furniture and historic decor, yet equipped with modern amenities. Ideal for clients who appreciate a touch of history in their meetings.",
        "location": "Philadelphia",
        "price_per_hour": 140,
        "status": "unavailable"
    },
    {
        "title": "Rooftop Event Space",
        "description": "An outdoor event space located on a rooftop, offering stunning city views. The space is perfect for parties, receptions, and other social events, with a stylish design and ample seating.",
        "location": "New Orleans",
        "price_per_hour": 220,
        "status": "available"
    },
    {
        "title": "Suburban Office Suite",
        "description": "A quiet and professional office suite located in a suburban area, providing a peaceful environment away from the hustle and bustle of the city. Perfect for teams that need focus and privacy.",
        "location": "Minneapolis",
        "price_per_hour": 120,
        "status": "unavailable"
    },
    {
        "title": "Industrial Loft",
        "description": "A unique loft space with an industrial design, featuring exposed brick, large windows, and an open floor plan. Ideal for creative projects, workshops, and team events.",
        "location": "Detroit",
        "price_per_hour": 200,
        "status": "available"
    },
    {
        "title": "Chic Downtown Studio",
        "description": "A bright and modern studio space located in the heart of the city. The space is perfect for photo and video shoots, with plenty of natural light and a clean, minimalist design.",
        "location": "San Antonio",
        "price_per_hour": 150,
        "status": "unavailable"
    },
    {
        "title": "Boutique Office",
        "description": "A small, stylish office space designed for professionals who appreciate quality and design. The space includes high-end furniture, a private meeting area, and a quiet atmosphere.",
        "location": "Phoenix",
        "price_per_hour": 100,
        "status": "available"
    },
    {
        "title": "High-Tech Conference Room",
        "description": "A conference room equipped with cutting-edge technology, including interactive displays, video conferencing capabilities, and smart whiteboards. Ideal for tech-savvy teams.",
        "location": "Silicon Valley",
        "price_per_hour": 280,
        "status": "available"
    },
    {
        "title": "Elegant Ballroom",
        "description": "A grand ballroom designed for elegant events, such as weddings, banquets, and galas. The space features high ceilings, crystal chandeliers, and a luxurious ambiance.",
        "location": "Orlando",
        "price_per_hour": 320,
        "status": "unavailable"
    },
    {
        "title": "Artistic Co-Working Space",
        "description": "An inspiring co-working environment designed for creative professionals. The space offers a mix of open desks, private studios, and collaborative areas, all within a vibrant and artistic setting.",
        "location": "Santa Fe",
        "price_per_hour": 110,
        "status": "available"
    },
    {
        "title": "Penthouse Office",
        "description": "A top-floor office space with panoramic views of the city. The space is luxurious and exclusive, featuring high-end furnishings, a private terrace, and premium amenities.",
        "location": "Las Vegas",
        "price_per_hour": 350,
        "status": "available"
    },
    {
        "title": "Seaside Conference Room",
        "description": "A conference room with stunning views of the ocean, creating a calm and inspiring environment for meetings. The space includes modern conferencing technology and comfortable seating.",
        "location": "Honolulu",
        "price_per_hour": 200,
        "status": "unavailable"
    },
    {
        "title": "Open-Air Event Space",
        "description": "An outdoor event space located in a beautiful garden setting, perfect for weddings, receptions, and other social gatherings. The space features lush greenery, a stylish design, and ample seating.",
        "location": "Savannah",
        "price_per_hour": 270,
        "status": "available"
    },
    {
        "title": "Creative Loft Space",
        "description": "A spacious loft designed for creative projects, such as art installations, photo shoots, and team brainstorms. The space offers an open layout, large windows, and a unique, industrial design.",
        "location": "Brooklyn",
        "price_per_hour": 180,
        "status": "unavailable"
    },
    {
        "title": "Downtown Private Office",
        "description": "A private office located in the heart of the city, offering convenience and style. The space is fully furnished with modern amenities and is ideal for professionals who need a central location.",
        "location": "Washington, D.C.",
        "price_per_hour": 220,
        "status": "available"
    },
    {
        "title": "Luxury Penthouse Event Space",
        "description": "An exclusive event space located in a penthouse, offering breathtaking views and a luxurious setting. Perfect for high-end events, receptions, and private gatherings.",
        "location": "Los Angeles",
        "price_per_hour": 400,
        "status": "available"
    },
    {
        "title": "Suburban Training Room",
        "description": "A training room located in a quiet suburban area, offering a peaceful environment for learning and development sessions. The space includes modern technology, flexible seating, and breakout areas.",
        "location": "Charlotte",
        "price_per_hour": 130,
        "status": "unavailable"
    },
    {
        "title": "High-Rise Office Suite",
        "description": "A premium office suite located on a high floor, offering stunning views of the city skyline. The space is perfect for businesses that need a prestigious and professional environment.",
        "location": "Houston",
        "price_per_hour": 240,
        "status": "available"
    },
    {
        "title": "Elegant Conference Room",
        "description": "A beautifully designed conference room, featuring elegant decor and modern technology. Ideal for meetings that require a touch of sophistication and style.",
        "location": "Chicago",
        "price_per_hour": 190,
        "status": "available"
    },
    {
        "title": "Vintage Event Space",
        "description": "A unique event space with a vintage charm, perfect for themed parties, weddings, and other special occasions. The space features antique furniture, classic decor, and a warm, inviting atmosphere.",
        "location": "Charleston",
        "price_per_hour": 210,
        "status": "unavailable"
    },
    {
        "title": "Modern Office Pod",
        "description": "A compact, modern office pod designed for solo work or small teams. The pod includes all necessary amenities, such as high-speed internet, ergonomic seating, and privacy screens.",
        "location": "San Francisco",
        "price_per_hour": 160,
        "status": "available"
    },
    {
        "title": "Spacious Workshop Venue",
        "description": "A large venue designed for workshops, seminars, and training sessions. The space includes flexible seating arrangements, modern presentation tools, and breakout areas for group work.",
        "location": "San Diego",
        "price_per_hour": 220,
        "status": "unavailable"
    },
    {
        "title": "Cozy Cottage Office",
        "description": "A charming cottage-style office space, perfect for creative work or small meetings. The space offers a peaceful, homely environment, with comfortable furnishings and a private garden.",
        "location": "Boulder",
        "price_per_hour": 150,
        "status": "available"
    },
    {
        "title": "Urban Event Loft",
        "description": "A stylish loft space located in the city, perfect for social events, receptions, and corporate gatherings. The space features an open floor plan, modern decor, and a rooftop terrace.",
        "location": "New York",
        "price_per_hour": 280,
        "status": "available"
    },
    {
        "title": "Chic Boutique Office",
        "description": "A small, elegant office space designed for professionals who value style and quality. The space includes high-end furniture, a private meeting room, and a quiet, focused environment.",
        "location": "Los Angeles",
        "price_per_hour": 170,
        "status": "unavailable"
    },
    {
        "title": "Historic Library Room",
        "description": "A meeting room located in a historic library, offering a unique and inspiring environment for discussions and meetings. The space features antique bookshelves, classic decor, and modern amenities.",
        "location": "Boston",
        "price_per_hour": 140,
        "status": "available"
    },
    {
        "title": "Beachfront Event Venue",
        "description": "A stunning event space located right on the beach, perfect for weddings, parties, and other special occasions. The space offers breathtaking views, a stylish design, and easy beach access.",
        "location": "Miami",
        "price_per_hour": 350,
        "status": "unavailable"
    },
    {
        "title": "Luxury Co-Working Space",
        "description": "A high-end co-working space designed for professionals who value luxury and convenience. The space includes private offices, open desks, and premium amenities, all within a sophisticated setting.",
        "location": "San Francisco",
        "price_per_hour": 200,
        "status": "available"
    },
    {
        "title": "Urban Workshop Loft",
        "description": "A spacious loft designed for workshops and creative projects, featuring an industrial design, flexible layouts, and modern amenities. Ideal for teams that need a versatile and inspiring environment.",
        "location": "Portland",
        "price_per_hour": 190,
        "status": "available"
    },
    {
        "title": "Penthouse Conference Room",
        "description": "An exclusive conference room located in a penthouse, offering panoramic views and a luxurious setting. The space is ideal for high-profile meetings, with premium amenities and a sophisticated ambiance.",
        "location": "New York",
        "price_per_hour": 370,
        "status": "unavailable"
    },
    {
        "title": "Modern Meeting Pod",
        "description": "A compact meeting pod designed for small team meetings or one-on-one discussions. The pod includes all necessary amenities, such as high-speed internet, comfortable seating, and privacy screens.",
        "location": "Seattle",
        "price_per_hour": 140,
        "status": "available"
    },
    {
        "title": "Trendy Downtown Loft",
        "description": "A chic loft space located in the downtown area, perfect for social events, creative projects, and corporate gatherings. The space features an open layout, modern decor, and a stylish design.",
        "location": "Los Angeles",
        "price_per_hour": 250,
        "status": "unavailable"
    },
    {
        "title": "Luxury Urban Studio",
        "description": "A luxurious studio space located in the city, designed for photo shoots, video production, and creative projects. The space offers high-end amenities, a stylish design, and excellent natural lighting.",
        "location": "San Francisco",
        "price_per_hour": 300,
        "status": "available"
    },
    {
        "title": "Rustic Lodge Event Space",
        "description": "A beautiful event space located in a rustic lodge, perfect for weddings, corporate retreats, and other special events. The space features wood-beamed ceilings, a cozy fireplace, and a scenic location.",
        "location": "Aspen",
        "price_per_hour": 280,
        "status": "available"
    }
]

        tenants = User.query.filter_by(role=UserRole.TENANT).all()
        for i in range(50):
            tenant = choice(tenants)
            space = space_list[i-1]
            title, description, location, price_per_hour, status = (space[key] for key in ['title', 'description', 'location', 'price_per_hour', 'status'])
            space = Space(
                title=title,
                description=description,
                location=location,
                price_per_hour=price_per_hour, 
                status=status,
                tenant_id=tenant.id
            )
            spaces.append(space)
        db.session.add_all(spaces)
        db.session.commit()
        print(f"Space data seeded successfully. Total spaces: {len(spaces)}")

        # Create booking data
        bookings = []
        users = User.query.filter_by(role=UserRole.USER).all()
        for _ in range(200):
            user_id = choice(users).id
            space_id = choice(range(1, 51))
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
            user = User.query.get(user_id)
            bookings = user.bookings
            if bookings:
                booking = choice(bookings)
                space_id = booking.space_id
                already_reviewed = any(review for review in reviews if review.user_id == user_id and review.space_id == space_id)
                if not already_reviewed:
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
        spaces = Space.query.filter_by(status='unavailable').all()
        for _ in range(50):
            if spaces:
                space = choice(spaces)
                space_id = space.id
                spaces.remove(space)
                event = Event(
                    title=fake.sentence(),
                    description=fake.text(max_nb_chars=200),
                    date=fake.future_date(),
                    organizer_id=choice(users).id,
                    space_id=space_id
                )
                events.append(event)
        db.session.add_all(events)
        db.session.commit()
        print(f"Events seeded successfully. Total events: {len(events)}")
