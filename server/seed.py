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
    num_users = 10 

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

        #Create space data
        categories = [
        "Meeting Room",
        "Event Venue",
        "Creative Studio",
        "Pop-Up Shop",
        "Workshop Space",
        "Outdoor Venue",
        "Private Dining Room"
        ]
        spaces = []
        space_list = [
    {
        "title": "Executive Conference Room",
        "description": "A spacious room designed for high-profile board meetings, featuring state-of-the-art conferencing equipment, ergonomic seating, and a stunning city view. Ideal for teams that require a professional and sophisticated environment.",
        "location": "New York",
        "price_per_hour": 200,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "Cozy Private Office",
        "description": "A comfortable and quiet private office space perfect for solo work or small teams. Equipped with modern office furniture, high-speed internet, and a peaceful atmosphere, making it ideal for productivity.",
        "location": "Los Angeles",
        "price_per_hour": 150,
        "status": "unavailable",
        "category": "Office Space"
    },
    {
        "title": "Grand Event Hall",
        "description": "A large, elegant event hall suitable for weddings, corporate events, and other large gatherings. Features include a grand stage, advanced lighting, and sound systems, as well as ample seating and catering facilities.",
        "location": "Chicago",
        "price_per_hour": 300,
        "status": "available",
        "category": "Event Venue"
    },
    {
        "title": "Modern Training Room",
        "description": "This room is designed for corporate training sessions and seminars. It comes equipped with modern audio-visual equipment, comfortable seating, and flexible layouts to accommodate various training needs.",
        "location": "Houston",
        "price_per_hour": 250,
        "status": "available",
        "category": "Workshop Space"
    },
    {
        "title": "Creative Studio",
        "description": "A versatile studio space perfect for photoshoots, video production, and creative projects. The space offers excellent natural lighting, a variety of backdrops, and high-quality soundproofing.",
        "location": "San Francisco",
        "price_per_hour": 180,
        "status": "unavailable",
        "category": "Creative Studio"
    },
    {
        "title": "Luxury Meeting Room",
        "description": "An upscale meeting room designed for executive meetings. The room features high-end furniture, advanced conferencing technology, and a luxurious ambiance that ensures a professional and comfortable environment.",
        "location": "Miami",
        "price_per_hour": 220,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "Shared Workspace",
        "description": "A flexible and collaborative co-working space that fosters creativity and networking. The space includes open desks, private booths, and breakout areas, all equipped with high-speed internet and modern amenities.",
        "location": "Austin",
        "price_per_hour": 80,
        "status": "available",
        "category": "Office Space"
    },
    {
        "title": "Private Workshop",
        "description": "This space is ideal for small group workshops, offering a quiet and focused environment. The workshop space includes flexible seating arrangements, presentation tools, and whiteboards.",
        "location": "Denver",
        "price_per_hour": 130,
        "status": "unavailable",
        "category": "Workshop Space"
    },
    {
        "title": "Tech Hub Conference Room",
        "description": "A state-of-the-art conference room located in the heart of the tech district. Equipped with the latest in conferencing technology, including video conferencing, large displays, and smart whiteboards.",
        "location": "San Jose",
        "price_per_hour": 210,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "Downtown Event Space",
        "description": "A centrally located event space perfect for corporate functions, social gatherings, and other events. The space features a modern design, flexible seating, and full catering services.",
        "location": "Boston",
        "price_per_hour": 250,
        "status": "unavailable",
        "category": "Event Venue"
    },
    {
        "title": "Creative Co-Working Space",
        "description": "A vibrant co-working environment designed for freelancers, startups, and small businesses. The space offers a mix of private offices, open desks, and collaborative areas, all within a creative and inspiring setting.",
        "location": "Portland",
        "price_per_hour": 90,
        "status": "available",
        "category": "Creative Studio"
    },
    {
        "title": "Beachside Conference Room",
        "description": "A unique conference room offering breathtaking ocean views. This space is ideal for meetings that require a calm and inspiring environment, complete with modern conferencing technology and comfortable seating.",
        "location": "San Diego",
        "price_per_hour": 190,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "Rustic Barn Event Venue",
        "description": "A charming venue located in a rustic barn, perfect for weddings, social events, and intimate gatherings. The space features exposed wooden beams, a spacious layout, and beautiful countryside views.",
        "location": "Nashville",
        "price_per_hour": 230,
        "status": "unavailable",
        "category": "Event Venue"
    },
    {
        "title": "Luxury Private Office",
        "description": "An exclusive private office with premium amenities, including high-speed internet, luxury furnishings, and a private meeting area. Perfect for professionals who require a high-end workspace.",
        "location": "Dallas",
        "price_per_hour": 260,
        "status": "available",
        "category": "Office Space"
    },
    {
        "title": "Modern Conference Suite",
        "description": "A suite of conference rooms designed for large meetings, workshops, and breakout sessions. The space includes modern technology, flexible seating arrangements, and catering options.",
        "location": "Atlanta",
        "price_per_hour": 300,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "Historic Meeting Room",
        "description": "A meeting room with a classic design, featuring antique furniture and historic decor, yet equipped with modern amenities. Ideal for clients who appreciate a touch of history in their meetings.",
        "location": "Philadelphia",
        "price_per_hour": 140,
        "status": "unavailable",
        "category": "Meeting Room"
    },
    {
        "title": "Rooftop Event Space",
        "description": "An outdoor event space located on a rooftop, offering stunning city views. The space is perfect for parties, receptions, and other social events, with a stylish design and ample seating.",
        "location": "New Orleans",
        "price_per_hour": 220,
        "status": "available",
        "category": "Outdoor Venue"
    },
    {
        "title": "Suburban Office Suite",
        "description": "A quiet and professional office suite located in a suburban area, providing a peaceful environment away from the hustle and bustle of the city. Perfect for teams that need focus and privacy.",
        "location": "Minneapolis",
        "price_per_hour": 120,
        "status": "unavailable",
        "category": "Office Space"
    },
    {
        "title": "Industrial Loft",
        "description": "A unique loft space with an industrial design, featuring exposed brick, large windows, and an open floor plan. Ideal for creative projects, workshops, and team events.",
        "location": "Detroit",
        "price_per_hour": 200,
        "status": "available",
        "category": "Creative Studio"
    },
    {
        "title": "High-Tech Conference Room",
        "description": "A conference room equipped with cutting-edge technology, including interactive displays, video conferencing capabilities, and smart whiteboards. Ideal for tech-savvy teams.",
        "location": "Silicon Valley",
        "price_per_hour": 280,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "Skyline Meeting Room",
        "description": "A sleek, modern space with floor-to-ceiling windows offering panoramic city views, ideal for board meetings and strategy sessions.",
        "location": "New York",
        "price_per_hour": 200,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "Green Park Outdoor Venue",
        "description": "An open outdoor venue surrounded by lush greenery, perfect for weddings, corporate events, and social gatherings.",
        "location": "San Francisco",
        "price_per_hour": 150,
        "status": "unavailable",
        "category": "Outdoor Venue"
    },
    {
        "title": "Historic Mansion Event Venue",
        "description": "A beautifully preserved mansion offering an elegant setting for upscale events, including weddings and private parties.",
        "location": "Boston",
        "price_per_hour": 350,
        "status": "available",
        "category": "Event Venue"
    },
    {
        "title": "Artistic Loft Studio",
        "description": "A spacious loft with high ceilings, natural light, and an industrial vibe, suitable for photoshoots, art exhibitions, and creative workshops.",
        "location": "Chicago",
        "price_per_hour": 120,
        "status": "available",
        "category": "Creative Studio"
    },
    {
        "title": "Cozy Private Dining Room",
        "description": "An intimate dining space with a warm ambiance, perfect for small gatherings, private dinners, and celebrations.",
        "location": "Seattle",
        "price_per_hour": 180,
        "status": "unavailable",
        "category": "Private Dining Room"
    },
    {
        "title": "Tech Hub Workshop Space",
        "description": "A dynamic and versatile space designed to inspire creativity and collaboration, ideal for tech meetups, hackathons, and innovation workshops.",
        "location": "San Jose",
        "price_per_hour": 250,
        "status": "available",
        "category": "Workshop Space"
    },
    {
        "title": "Contemporary Office Space",
        "description": "A fully furnished office space with modern amenities, perfect for freelancers, startups, and small businesses looking for a professional environment.",
        "location": "Austin",
        "price_per_hour": 100,
        "status": "unavailable",
        "category": "Office Space"
    },
    {
        "title": "Minimalist Meeting Space",
        "description": "A simple and clean meeting space designed for maximum productivity. The space is equipped with essential meeting tools and comfortable seating, offering a distraction-free environment.",
        "location": "Salt Lake City",
        "price_per_hour": 110,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "Urban Art Studio",
        "description": "A vibrant and colorful studio space located in the heart of the city's arts district. Ideal for artists, photographers, and creative professionals who need an inspiring space to work.",
        "location": "Los Angeles",
        "price_per_hour": 160,
        "status": "unavailable",
        "category": "Creative Studio"
    },
    {
        "title": "High-Rise Conference Room",
        "description": "A modern conference room located in a high-rise building, offering panoramic views of the city. The space is equipped with the latest conferencing technology and elegant furnishings.",
        "location": "Manhattan",
        "price_per_hour": 260,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "Zen Garden Meeting Room",
        "description": "A tranquil meeting room that overlooks a beautiful zen garden. The space is designed to promote calmness and focus, making it perfect for brainstorming sessions and strategy meetings.",
        "location": "Portland",
        "price_per_hour": 190,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "The Rustic Barn",
        "description": "An old barn converted into a unique event space. With its rustic charm and modern amenities, it's ideal for those looking to host an event with a blend of old and new.",
        "location": "Dallas",
        "price_per_hour": 150,
        "status": "available",
        "category": "Event Venue"
    },
    {
        "title": "The Urban Loft",
        "description": "A loft-style venue located in the heart of the city, featuring exposed brick walls, high ceilings, and an industrial chic aesthetic. Perfect for art exhibitions, pop-up events, and photo shoots.",
        "location": "New York",
        "price_per_hour": 250,
        "status": "available",
        "category": "Creative Studio"
    },
    {
        "title": "Suburban Retreat",
        "description": "A quiet retreat away from the hustle and bustle of the city. This venue features lush gardens and a tranquil pond, making it an ideal spot for weddings, retreats, and intimate gatherings.",
        "location": "Chicago",
        "price_per_hour": 180,
        "status": "unavailable",
        "category": "Outdoor Venue"
    },
    {
        "title": "Artistic Co-Working Space",
        "description": "An inspiring co-working environment designed for creative professionals. The space offers a mix of open desks, private studios, and collaborative areas, all within a vibrant and artistic setting.",
        "location": "Santa Fe",
        "price_per_hour": 110,
        "status": "available",
        "category": "Creative Studio"
    },
    {
        "title": "Seaside Conference Room",
        "description": "A conference room with stunning views of the ocean, creating a calm and inspiring environment for meetings. The space includes modern conferencing technology and comfortable seating.",
        "location": "Honolulu",
        "price_per_hour": 200,
        "status": "unavailable",
        "category": "Meeting Room"
    },
    {
        "title": "Open-Air Event Space",
        "description": "An outdoor event space located in a beautiful garden setting, perfect for weddings, receptions, and other social gatherings. The space features lush greenery, a stylish design, and ample seating.",
        "location": "Savannah",
        "price_per_hour": 270,
        "status": "available",
        "category": "Outdoor Venue"
    },
    {
        "title": "Luxury Penthouse Event Space",
        "description": "An exclusive event space located in a penthouse, offering breathtaking views and a luxurious setting. Perfect for high-end events, receptions, and private gatherings.",
        "location": "Los Angeles",
        "price_per_hour": 400,
        "status": "available",
        "category": "Event Venue"
    },
    {
        "title": "High-Rise Office Suite",
        "description": "A premium office suite located on a high floor, offering stunning views of the city skyline. The space is perfect for businesses that need a prestigious and professional environment.",
        "location": "Houston",
        "price_per_hour": 240,
        "status": "available",
        "category": "Office Space"
    },
    {
        "title": "Spacious Workshop Venue",
        "description": "A large venue designed for workshops, seminars, and training sessions. The space includes flexible seating arrangements, modern presentation tools, and breakout areas for group work.",
        "location": "San Diego",
        "price_per_hour": 220,
        "status": "unavailable",
        "category": "Workshop Space"
    },
    {
        "title": "Cozy Cottage Office",
        "description": "A charming cottage-style office space, perfect for creative work or small meetings. The space offers a peaceful, homely environment, with comfortable furnishings and a private garden.",
        "location": "Boulder",
        "price_per_hour": 150,
        "status": "available",
        "category": "Office Space"
    },
    {
        "title": "Chic Boutique Office",
        "description": "A small, elegant office space designed for professionals who value style and quality. The space includes high-end furniture, a private meeting room, and a quiet, focused environment.",
        "location": "Los Angeles",
        "price_per_hour": 170,
        "status": "unavailable",
        "category": "Office Space"
    },
    {
        "title": "Beachfront Event Venue",
        "description": "A stunning event space located right on the beach, perfect for weddings, parties, and other special occasions. The space offers breathtaking views, a stylish design, and easy beach access.",
        "location": "Miami",
        "price_per_hour": 350,
        "status": "unavailable",
        "category": "Event Venue"
    },
    {
        "title": "Modern Meeting Pod",
        "description": "A compact meeting pod designed for small team meetings or one-on-one discussions. The pod includes all necessary amenities, such as high-speed internet, comfortable seating, and privacy screens.",
        "location": "Seattle",
        "price_per_hour": 140,
        "status": "available",
        "category": "Meeting Room"
    },
    {
        "title": "Trendy Downtown Loft",
        "description": "A chic loft space located in the downtown area, perfect for social events, creative projects, and corporate gatherings. The space features an open layout, modern decor, and a stylish design.",
        "location": "Los Angeles",
        "price_per_hour": 250,
        "status": "unavailable",
        "category": "Creative Studio"
    },
    {
        "title": "Luxury Urban Studio",
        "description": "An upscale studio space designed for creative professionals. The space includes private studios, collaborative areas, and premium amenities, all within a luxurious urban setting.",
        "location": "San Francisco",
        "price_per_hour": 210,
        "status": "available",
        "category": "Creative Studio"
    },
    {
        "title": "Suburban Office Suite",
        "description": "A professional office suite located in a suburban area, offering a peaceful and convenient work environment. The space is fully furnished with modern amenities, ideal for businesses that need a suburban location.",
        "location": "Dallas",
        "price_per_hour": 180,
        "status": "available",
        "category": "Office Space"
    },
    {
        "title": "Coastal Creative Space",
        "description": "A creative space located near the coast, offering a relaxing and inspiring environment for creative work. The space includes private studios, collaborative areas, and easy access to the beach.",
        "location": "San Diego",
        "price_per_hour": 190,
        "status": "unavailable",
        "category": "Creative Studio"
    },
    {
        "title": "Historic Downtown Office",
        "description": "A charming office space located in a historic building downtown, offering a unique and professional work environment. The space includes modern amenities, private offices, and a stylish design.",
        "location": "Boston",
        "price_per_hour": 200,
        "status": "available",
        "category": "Office Space"
    },
    {
        "title": "Luxury Beachside Studio",
        "description": "An exclusive studio space located by the beach, perfect for creative projects, photo shoots, and private events. The space features a modern design, premium amenities, and stunning ocean views.",
        "location": "Malibu",
        "price_per_hour": 330,
        "status": "unavailable",
        "category": "Creative Studio"
    }
]

        tenants = User.query.filter_by(role=UserRole.TENANT).all()
        for i in range(50):
            tenant = choice(tenants)
            space = space_list[i-1]
            title, description, location, price_per_hour, status, category = (space[key] for key in ['title', 'description', 'location', 'price_per_hour', 'status', 'category'])
            space = Space(
                title=title,
                description=description,
                location=location,
                price_per_hour=price_per_hour, 
                status=status,
                tenant_id=tenant.id, 
                category=category
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
            created_at = fake.date_this_year()

            booking = Booking(
                user_id=user_id,
                space_id=space_id,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
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

        # Sample users and spaces
        users = User.query.all()
        spaces = Space.query.filter_by(status='unavailable').all()

        # Manually defining 50 sample events
        sample_events = [
            {
                "title": "Summer Networking Event",
                "description": "Join us for a fun networking event with industry professionals.",
                "date": date(2024, 8, 20),
                "image_url": "https://example.com/images/networking.jpg"
            },
            {
                "title": "Tech Innovation Conference",
                "description": "A conference discussing the latest trends in technology and innovation.",
                "date": date(2024, 9, 10),
                "image_url": "https://example.com/images/tech_conference.jpg"
            },
            {
                "title": "Art and Design Expo",
                "description": "Explore the world of art and design at our annual expo.",
                "date": date(2024, 10, 5),
                "image_url": "https://example.com/images/art_expo.jpg"
            },
            {
                "title": "Business Growth Summit",
                "description": "Learn strategies for growing your business at our annual summit.",
                "date": date(2024, 9, 25),
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
                "date": date(2024, 8, 15),
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
                "date": date(2024, 11, 22),
                "image_url": "https://example.com/images/film_screening.jpg"
            },
            {
                "title": "Charity Fundraising Gala",
                "description": "Support a great cause by attending our charity fundraising gala.",
                "date": date(2024, 8, 25),
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
                "date": date(2024, 8, 18),
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
                "date": date(2024, 10, 30),
                "image_url": "https://example.com/images/meditation_retreat.jpg"
            },
            {
                "title": "Fitness Challenge Event",
                "description": "Participate in our fitness challenge and push your limits.",
                "date": date(2024, 8, 15),
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
                "date": date(2024, 11, 26),
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
                "date": date(2024, 8, 22),
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
                "date": date(2024, 8, 20),
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
                "date": date(2024, 8, 27),
                "image_url": "https://example.com/images/cider_tasting.jpg"
            },
            {
                "title": "Literary Salon",
                "description": "Join authors for a discussion on literature and writing.",
                "date": date(2024, 8, 14),
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
        print(f"Events seeded successfully. Total events: {len(events)}")
        
        
        
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
                    "data:image/jpeg;base64,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",
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
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqxrzw3sRFwoMy2teoaO_oedw6-EbasiLEbQ&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsv5BghQypAA9vL-F_dueyDaJmYiYCsfyZUA&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0q1-ZXX1ueiy5mmfD8HkhEt6Sc_jNf4xeNg&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT27H5Kc3MuLwzQMvZdT76_yeiEgabghpwpSw&s",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1644623443707-S7228HXVYZ1LTB8V3CLD/Ovation+Space+Lounge.jpg?format=1000w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1644623533162-TEJHCRQWOWR01198J2PW/DSC03272-min.jpg?format=1500w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1644623527196-8HHM5R9D8DWNQ53R98BI/DSC03005-min.jpg?format=1500w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1644623537643-LFTCOX3ASNOJAQ5DV3Z0/PRM_7413-min.jpg?format=1500w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1644623527241-61N1A87WPTMLOYUXFJDM/DSC03007-min.jpg?format=1500w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1644623535683-U7KRUSGVEIZQD0RPV6V9/PRM_7362-min.jpg?format=1500w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1632529722181-BVEIFVUOKDAIRTRWA2DI/20210915-154434-OVATION-03102-min-min.jpg?format=1500w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1632529770837-YYVUBXL7Z01GC45KXLSN/20210915-113426-OVATION-02980.jpg?format=1500w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1632529730202-DJB5HLTK4MQUCCL2DRQB/20210915-142543-OVATION-02997-min-min.jpg?format=1500w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1632529662447-D3UJFPCNJORHHCZKK7KA/20210915-151359-OVATION-03048-min-min.jpg?format=1500w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1632529707423-I54VZVZTN10H0FDEKT50/20210915-114147-OVATION-02986.jpg?format=1500w",
                    "https://images.squarespace-cdn.com/content/v1/5c53611a0cf57d7ce300be61/1674029215252-X9IZHI9U9ACYNPH9JEHE/20210915-111526-OVATION-02950+%281%29.jpg?format=1500w",
                    "https://cdn-images.wework.com/images/53CDDEE4-ECB8-11EC-955D-0E6A5DC689CD/53cddee4-ecb8-11ec-955d-0e6a5dc689cd_1.jpg?width=800",
                    "https://cdn-images.wework.com/images/54230F5E-ECB8-11EC-9560-0E6A5DC689CD/54230f5e-ecb8-11ec-9560-0e6a5dc689cd_4.jpg?width=800",
                    "https://cdn-images.wework.com/images/2D703660-0FBC-11EA-A9A9-0A5BC5747799/2d703660-0fbc-11ea-a9a9-0a5bc5747799_6.jpg?width=800",
                    "https://cdn-images.wework.com/images/0956290C-9647-11EB-8C4B-0E6A5DC689CD/0956290c-9647-11eb-8c4b-0e6a5dc689cd_1.jpg?width=800",
                    "https://headbox-media.imgix.net/spaces/40712/photos/79d0fe73-888d-41ea-bdb3-bdcb506dda72_0071.jpg?auto=format&q=60&ixlib=react-9.5.4&w=1946",
                    "https://headbox-media.imgix.net/spaces/40712/photos/97a223dd-1c89-40be-bb14-961d17b745de_somewhere%20nowhere%204.jpeg?auto=format&q=60&ixlib=react-9.5.4&w=1946",
                    "https://headbox-media.imgix.net/spaces/40712/photos/8784b816-a3fd-4324-b6c4-70ff50ce5f4d_0081.jpg?auto=format&q=60&ixlib=react-9.5.4&w=1946",
                    "https://headbox-media.imgix.net/spaces/40712/photos/592712c5-856c-4648-bddc-f3164ecdd4f8_0091.jpg?auto=format&q=60&ixlib=react-9.5.4&w=1946",
                    "https://headbox-media.imgix.net/spaces/43833/photos/95596307-440e-46e0-a663-072d98526d48_IP1222_TheNedNoMad_Rooftop2_Hero.jpg?auto=format&q=60&ixlib=react-9.5.4&w=1946",
                    "https://headbox-media.imgix.net/spaces/43833/photos/5c102580-5ca1-4eb5-92b8-730bef6ef899_Rooftop4.jpg?auto=format&q=60&ixlib=react-9.5.4&w=1946",
                    "https://headbox-media.imgix.net/spaces/43262/photos/6b716fea-2b4b-47e4-8670-382ce750eee7_IMG_4645.jpg?auto=format&q=60&ixlib=react-9.5.4&w=1946",
                    "https://headbox-media.imgix.net/spaces/43262/photos/9a0320e1-3a20-470f-afff-9295481a6798_IMG_4641.jpg?auto=format&q=60&ixlib=react-9.5.4&w=1946",
                    "https://headbox-media.imgix.net/spaces/43262/photos/0e008120-3edc-405c-80fb-cd493189bad5_thumbnail_IMG_5240.jpg?auto=format&q=60&ixlib=react-9.5.4&w=1946",
                    "https://headbox-media.imgix.net/spaces/43262/photos/660a3c3f-dc66-4106-88ff-aec285d8411a_thumbnail_IMG_5225.jpg?auto=format&q=60&ixlib=react-9.5.4&w=1946",
                    "https://thevendry.com/cdn-cgi/image/height=1920,width=1920,fit=contain,metadata=none/https%3A%2F%2Fs3.amazonaws.com%2Fuploads.thevendry.co%2F23052%2F1654538602640_gallery-img-46.jpg",
                    "https://thevendry.com/cdn-cgi/image/height=1920,width=1920,fit=contain,metadata=none/https%3A%2F%2Fs3.amazonaws.com%2Fuploads.thevendry.co%2F1907%2F1569610094292_FromParriswithLove_OWO_Monthblanc-27.jpg",
                    "https://thevendry.com/cdn-cgi/image/height=1920,width=1920,fit=contain,metadata=none/https%3A%2F%2Fs3.amazonaws.com%2Fuploads.thevendry.co%2F23052%2F1654538854471_gallery-img-30.jpg",
                    "https://thevendry.com/cdn-cgi/image/height=1920,width=1920,fit=contain,metadata=none/https%3A%2F%2Fs3.amazonaws.com%2Fuploads.thevendry.co%2F1907%2F1569611180794_Edited-and-flipped.jpg",
                    "https://thevendry.com/cdn-cgi/image/height=1920,width=1920,fit=contain,metadata=none/https%3A%2F%2Fs3.amazonaws.com%2Fuploads.thevendry.co%2F1907%2F1569611200121_1185-M4154-Hechler.jpg",
                    "https://www.executivecentre.com/_next/image/?url=https%3A%2F%2Fassets.executivecentre.com%2Fassets%2FES-Venue-JPT-L14-EventSpace_Featured.jpg&w=1080&q=75",
                    "https://www.executivecentre.com/_next/image/?url=https%3A%2F%2Fassets.executivecentre.com%2Fassets%2FES-Venue-JPT-L14-EventSpace_Lounge.jpg&w=1080&q=75",
                    "https://www.executivecentre.com/_next/image/?url=https%3A%2F%2Fassets.executivecentre.com%2Fassets%2FES-Venue-JPT-L14-EventSpace_Coworking.jpg&w=1080&q=75",
                    "https://www.executivecentre.com/_next/image/?url=https%3A%2F%2Fassets.executivecentre.com%2Fassets%2FES-Venue-JPT-L14-EventSpace_Coworking.jpg&w=1080&q=75",
                    "https://www.executivecentre.com/_next/image/?url=https%3A%2F%2Fassets.executivecentre.com%2Fassets%2FES-Venue-ARC-L7EventSpace-BaristaBar.jpg&w=1080&q=75",
                    "https://www.executivecentre.com/_next/image/?url=https%3A%2F%2Fassets.executivecentre.com%2Fassets%2FES-Venue-ARC-L7EventSpace-Breakout.jpg&w=1080&q=75",
                    "https://www.executivecentre.com/_next/image/?url=https%3A%2F%2Fassets.executivecentre.com%2Fassets%2FES-Venue-ARC-L7EventSpace-BarTable.jpg&w=1080&q=75",
                    "https://s3-media0.fl.yelpcdn.com/bphoto/Zq4Y-NjtnOUU-0hMFmxOhQ/o.jpg",
                    "https://s3-media0.fl.yelpcdn.com/bphoto/b1l6VLYpB-YPdSsR29IhBQ/o.jpg",
                    "https://s3-media0.fl.yelpcdn.com/bphoto/H4a8CF0oQPYUR18ZSKtOJw/o.jpg",
                    ]
        spaces = Space.query.limit(20).all()
        for space in spaces:
            print(space)

            if len(space_images) >= 4:
                assigned_images = space_images[:4]
                space_images = space_images[4:]  
                for img_url in assigned_images:
                    space_image = SpaceImages(
                        space_id=space.id,
                        image_url=img_url
                    )
                    db.session.add(space_image)
            else:
                print("Not enough images left for assignment.")

        db.session.commit()
        print(f"Space image data seeded successfully. Total remaining space images: {len(space_images)}")

