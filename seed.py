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
                "date": date(2024, 8, 19),  # Adjusted to 19/08/2024
                "image_url": "https://cdn.pixabay.com/photo/2016/11/23/15/48/audience-1853662_640.jpg"
            },
            {
                "title": "Tech Innovation Conference",
                "description": "A conference discussing the latest trends in technology and innovation.",
                "date": date(2024, 8, 25),  # Adjusted to 25/08/2024
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMe96cCMh-AUL4BPEVI5HbRIscCu0sTky6kY6xKiS_r5sYYvA7VVIL729lenDbwCUr-3Y&usqp=CAU"
            },
            {
                "title": "Art and Design Expo",
                "description": "Explore the world of art and design at our annual expo.",
                "date": date(2024, 9, 5),  # Adjusted to 05/09/2024
                "image_url": "https://static.vecteezy.com/system/resources/thumbnails/028/884/486/small/generative-ai-people-crowd-on-music-rock-festival-concert-in-stadium-big-stage-lit-by-spotlights-photo.jpg"
            },
            {
                "title": "Business Growth Summit",
                "description": "Learn strategies for growing your business at our annual summit.",
                "date": date(2024, 9, 12),  # Adjusted to 12/09/2024
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLlIsYZLwRguhCmNpUr81LFPziI-gBx_CvtqTYNyBIf6E38wh6iFHshwPtulOruPEyrX4&usqp=CAU"
            },
            {
                "title": "Health and Wellness Fair",
                "description": "A fair dedicated to promoting health and wellness in the community.",
                "date": date(2024, 11, 15),
                "image_url": "data:image/jpeg;base64,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"
            },
            {
                "title": "Music Festival Extravaganza",
                "description": "Experience live music from top artists at our annual festival.",
                "date": date(2024, 10, 12),
                "image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpMQbFQC85MhP5AXY_hQoiRk-44WKPnyiEqg&s"
            },
            {
                "title": "Culinary Arts Showcase",
                "description": "Taste and learn from the best chefs in the culinary world.",
                "date": date(2024, 9, 5),
                "image_url": "data:image/jpeg;base64,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g"
            },
            {
                "title": "Startup Pitch Night",
                "description": "Watch startups pitch their innovative ideas to potential investors.",
                "date": date(2024, 9, 18),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnESlbrjo1Me2a1pyrSNpDA_kJ3CTLx6NGU_ULIv3PfPlz6sdlGJC43D3DRAp4lnq96hY&usqp=CAU"
            },
            {
                "title": "Fashion Week Gala",
                "description": "Celebrate the latest trends in fashion with top designers.",
                "date": date(2024, 10, 2),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRdGY5eaHlGtNlkds-akju77BbPJghHRIpL3rmdJM66NV6dYmFkmIqYY9yVt9Rmkua2V4&usqp=CAU"
            },
            {
                "title": "Environmental Awareness Conference",
                "description": "Discuss the challenges and solutions for environmental sustainability.",
                "date": date(2024, 11, 10),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDn59OdbwW-DXP1pXCCdql0OEsoIXHpPYfoA&s"
            },
            {
                "title": "Film Screening and Discussion",
                "description": "Join us for a film screening followed by a panel discussion.",
                "date": date(2024, 12, 22),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTaAYR5AwUSfStGFTPQv0-rP-mFyHb-3gB0Rk5bgnVEzH962yt0cjdmUEVtbc5WeC8Hfn0&usqp=CAU"
            },
            {
                "title": "Charity Fundraising Gala",
                "description": "Support a great cause by attending our charity fundraising gala.",
                "date": date(2024, 9, 25),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQb76lyUNrptZkiXrgMf3qIm16CZc2n0gS2Wg&s"
            },
            {
                "title": "Outdoor Adventure Expo",
                "description": "Explore outdoor gear and activities at our adventure expo.",
                "date": date(2024, 9, 7),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR582BTl21HoczUqXuWveyAYGYiYAVQqobpWYaN5sYzr9eHNhHnkfDgg1KW6qSLrXQBnoo&usqp=CAU"
            },
            {
                "title": "Photography Workshop",
                "description": "Improve your photography skills with expert guidance.",
                "date": date(2024, 10, 12),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQT6Sf41qnirUnfVhE6k08FwHK3gWkdMH6fk2YqCmXMCn4KKekrQiI2NPkRNYchHpjrhn4&usqp=CAU"
            },
            {
                "title": "Book Fair and Author Meet",
                "description": "Meet your favorite authors and discover new books at our fair.",
                "date": date(2024, 11, 2),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQT6Sf41qnirUnfVhE6k08FwHK3gWkdMH6fk2YqCmXMCn4KKekrQiI2NPkRNYchHpjrhn4&usqp=CAU"
            },
            {
                "title": "Startup Expo",
                "description": "Showcase your startup and connect with investors and customers.",
                "date": date(2024, 9, 18),
                "image_url": "https://media.istockphoto.com/id/1183245247/photo/concert-crowd-in-front-of-a-live-stage.jpg?b=1&s=612x612&w=0&k=20&c=6ORN82XcjQ-konti9L7IhjBD9jyDOsRCckLAcXYaiQE="
            },
            {
                "title": "Cultural Festival",
                "description": "Celebrate diverse cultures with music, dance, and food.",
                "date": date(2024, 9, 25),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5cL3iSA3ga7G0T2MMcIJ8hJZxC-R-pzGYZ8aVz5aXkEm84SzbR78tQBrE5ZMfF2xHGiw&usqp=CAU"
            },
            {
                "title": "Tech Bootcamp",
                "description": "Learn the latest technology skills in an intensive bootcamp.",
                "date": date(2024, 10, 5),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCOKkVupE24szjYHWAzMBtK-mY8uMen_mAULrIZxgPz_Pomj5IqlI-gFW7p9Sy1wDW0Tc&usqp=CAU"
            },
            {
                "title": "Science Symposium",
                "description": "Discuss groundbreaking research and discoveries in science.",
                "date": date(2024, 11, 20),
                "image_url": "data:image/jpeg;base64,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"
            },
            {
                "title": "Meditation and Mindfulness Retreat",
                "description": "Find peace and relaxation at our meditation retreat.",
                "date": date(2024, 9, 30),
                "image_url": "data:image/jpeg;base64,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"
            },
            {
                "title": "Fitness Challenge Event",
                "description": "Participate in our fitness challenge and push your limits.",
                "date": date(2024, 9, 15),
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcIAN1DutyXh9T2eHXbS5RMlv7zj6UFNHWzT9triUhUXUMdPXbnUTvriOxlkqrnWuaqds&usqp=CAU"
            },
            {
                "title": "Wine Tasting Event",
                "description": "Sample a variety of wines at our exclusive tasting event.",
                "date": date(2024, 9, 10),
                "image_url": "https://i.pinimg.com/564x/ce/ff/3d/ceff3d1743ad3e000234e87f217085e4.jpg"
            },
            {
                "title": "Craft and Handmade Fair",
                "description": "Discover unique handmade crafts and goods at our fair.",
                "date": date(2024, 10, 8),
                "image_url": "https://i.pinimg.com/236x/02/7f/23/027f2321da050a372eb070e563d73abc.jpg"
            },
            {
                "title": "Outdoor Movie Night",
                "description": "Enjoy a classic movie under the stars at our outdoor screening.",
                "date": date(2024, 11, 3),
                "image_url": "https://i.pinimg.com/236x/4c/40/0a/4c400acd3e25bf2ed939724529bfe55e.jpg"
            },
            {
                "title": "Dance Workshop",
                "description": "Learn new dance moves from professional instructors.",
                "date": date(2024, 9, 14),
                "image_url": "https://i.pinimg.com/236x/aa/8c/1b/aa8c1b1c61cf1c1dc28c4d3b31fd9a3c.jpg"
            },
            {
                "title": "Yoga and Wellness Retreat",
                "description": "Rejuvenate your body and mind at our yoga retreat.",
                "date": date(2024, 8, 22),
                "image_url": "https://i.pinimg.com/236x/71/36/72/7136721d260db686f84abb6b32811c4b.jpg"
            },
            {
                "title": "Sustainability Workshop",
                "description": "Learn how to live a more sustainable lifestyle.",
                "date": date(2024, 9, 29),
                "image_url": "https://i.pinimg.com/236x/b2/75/33/b27533b4177c41545dfb178aa16f2ff7.jpg"
            },
            {
                "title": "Startup Networking Night",
                "description": "Connect with fellow entrepreneurs at our networking night.",
                "date": date(2024, 10, 15),
                "image_url": "https://i.pinimg.com/236x/e3/b8/25/e3b8258e2c1bbda405ca0ec4dbf608dd.jpg"
            },
            {
                "title": "Food Truck Festival",
                "description": "Sample delicious food from the best food trucks in town.",
                "date": date(2024, 11, 12),
                "image_url": "https://i.pinimg.com/236x/9d/4a/8b/9d4a8b142d12df886d0905264978bf63.jpg"
            },
            {
                "title": "Digital Marketing Conference",
                "description": "Stay ahead of the trends in digital marketing.",
                "date": date(2024, 10, 26),
                "image_url": "https://i.pinimg.com/236x/c4/9f/bd/c49fbd16d2df3ee3c07fcc142df65d1e.jpg"
            },
            {
                "title": "Gardening Expo",
                "description": "Learn tips and tricks for your garden at our expo.",
                "date": date(2024, 8, 28),
                "image_url": "https://i.pinimg.com/236x/ff/56/38/ff56386fe47170b45d912448ce738a46.jpg"
            },
            {
                "title": "Outdoor Yoga Session",
                "description": "Join us for a refreshing outdoor yoga session.",
                "date": date(2024, 9, 12),
                "image_url": "https://i.pinimg.com/236x/e4/6d/af/e46daf53e208be379ee5588f1f8e11c9.jpg"
            },
            {
                "title": "Artisan Market",
                "description": "Shop unique handmade goods at our artisan market.",
                "date": date(2024, 10, 20),
                "image_url": "https://i.pinimg.com/236x/85/1b/fe/851bfe22f46daa260ccb5a68c7c6ec22.jpg"
            },
            {
                "title": "Coding Hackathon",
                "description": "Test your coding skills in our 24-hour hackathon.",
                "date": date(2024, 11, 7),
                "image_url": "https://i.pinimg.com/236x/79/6d/9d/796d9d1737a8a312ef1307622e7e47ff.jpg"
            },
            {
                "title": "Wine and Cheese Evening",
                "description": "Enjoy an evening of wine and cheese pairing.",
                "date": date(2024, 9, 18),
                "image_url": "https://i.pinimg.com/236x/f7/e5/3c/f7e53c57dc40cfe95e1c4289a760cc0d.jpg"
            },
            {
                "title": "Baking Workshop",
                "description": "Learn how to bake delicious treats from professional bakers.",
                "date": date(2024, 9, 12),
                "image_url": "https://i.pinimg.com/236x/b2/75/33/b27533b4177c41545dfb178aa16f2ff7.jpg"
            },
            {
                "title": "Sustainable Fashion Show",
                "description": "Explore the latest in sustainable fashion at our show.",
                "date": date(2024, 9, 3),
                "image_url": "https://i.pinimg.com/236x/10/44/95/104495de95667b4c78c550de55d9743f.jpg"
            },
            {
                "title": "Film Festival",
                "description": "Watch award-winning films at our annual film festival.",
                "date": date(2024, 10, 1),
                "image_url": "https://i.pinimg.com/236x/a8/c9/25/a8c925bf5f6691cdcbc483882ebea376.jpg"
            },
            {
                "title": "Tech Talks Seminar",
                "description": "Listen to experts discuss the latest in technology.",
                "date": date(2024, 11, 17),
                "image_url": "https://i.pinimg.com/236x/10/44/95/104495de95667b4c78c550de55d9743f.jpg"
            },
            {
                "title": "Craft Beer Tasting",
                "description": "Sample a variety of craft beers from local breweries.",
                "date": date(2024, 10, 20),
                "image_url": "https://i.pinimg.com/236x/3c/18/ce/3c18ce803ebc7c75c4b4d1054575acc1.jpg"
            },
            {
                "title": "Culinary Experience",
                "description": "Enjoy a multi-course meal prepared by top chefs.",
                "date": date(2024, 8, 30),
                "image_url": "https://i.pinimg.com/236x/28/22/30/282230b729e3fc96382a52ea481ea4e2.jpg"
            },
            {
                "title": "Startup Founders Meetup",
                "description": "Meet and learn from successful startup founders.",
                "date": date(2024, 9, 9),
                "image_url": "https://i.pinimg.com/236x/60/42/0a/60420a16ff6103350728fc6da770c389.jpg"
            },
            {
                "title": "Holiday Market",
                "description": "Shop for unique holiday gifts at our holiday market.",
                "date": date(2024, 12, 5),
                "image_url": "https://i.pinimg.com/236x/c6/88/f6/c688f6bfb24174445ed9d51d34c4027b.jpg"
            },
            {
                "title": "Blockchain Seminar",
                "description": "Learn about the impact of blockchain technology.",
                "date": date(2024, 10, 17),
                "image_url": "hhttps://i.pinimg.com/736x/f3/28/ac/f328acadb73c977e6de7291abeed1b73.jpg"
            },
            {
                "title": "Outdoor Art Fair",
                "description": "Discover local artists and their work at our outdoor fair.",
                "date": date(2024, 11, 21),
                "image_url": "https://i.pinimg.com/236x/2b/f3/5d/2bf35d778e25f7f8f17d55c68b548b3c.jpg"
            },
            {
                "title": "Cider Tasting Event",
                "description": "Taste a variety of ciders at our tasting event.",
                "date": date(2024, 9, 27),
                "image_url": "https://i.pinimg.com/236x/8f/56/98/8f56983b3d38785786ecd769f53ebd22.jpg"
            },
            {
                "title": "Literary Salon",
                "description": "Join authors for a discussion on literature and writing.",
                "date": date(2024, 9, 14),
                "image_url": "https://i.pinimg.com/236x/1b/47/ba/1b47bae30b12f7e8a6cc6bddf0a2a354.jpg"
            },
            {
                "title": "Startup Workshop",
                "description": "Learn how to launch and scale your startup.",
                "date": date(2024, 9, 24),
                "image_url": "https://i.pinimg.com/236x/92/1f/68/921f68e3d0fe88fd2204647f73d74541.jpg"
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
                    "https://images.pexels.com/photos/37347/office-sitting-room-executive-sitting.jpg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/2883049/pexels-photo-2883049.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/3778619/pexels-photo-3778619.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/273671/pexels-photo-273671.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/416320/pexels-photo-416320.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/380768/pexels-photo-380768.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/2451566/pexels-photo-2451566.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/633269/pexels-photo-633269.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/3778619/pexels-photo-3778619.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/2451616/pexels-photo-2451616.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/2678468/pexels-photo-2678468.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/273671/pexels-photo-273671.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/1181396/pexels-photo-1181396.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/1181395/pexels-photo-1181395.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://images.pexels.com/photos/845451/pexels-photo-845451.jpeg?auto=compress&cs=tinysrgb&w=800",
                    "https://media.istockphoto.com/id/883792980/photo/white-and-glass-office-interior.jpg?s=1024x1024&w=is&k=20&c=c8hCoRnmNbVhF3v53G8VWepCDEv9GEWbTH1sQaftok4=",
                    "https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8b2ZmaWNlfGVufDB8fDB8fHww",
                    "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8b2ZmaWNlfGVufDB8fDB8fHww",
                    "https://images.unsplash.com/photo-1531973576160-7125cd663d86?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fG9mZmljZXxlbnwwfHwwfHx8MA%3D%3D",
                    "https://media.istockphoto.com/id/1591225732/photo/modern-open-plan-office-space-with-tables-office-chairs-creeper-plants-and-manager-room.webp?b=1&s=612x612&w=0&k=20&c=O9QQtaNJQlebyoykA9WEC9RW6eub8GXbHcRrxVPSnX8=",
                    "https://images.unsplash.com/photo-1655746340587-9d1aaad92b6d?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8b2ZmaWNlJTIwYmFja2dyb3VuZHxlbnwwfHwwfHx8MA%3D%3D",
                    "https://images.unsplash.com/photo-1716635174919-e6aec2d1c45a?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8b2ZmaWNlJTIwYmFja2dyb3VuZHxlbnwwfHwwfHx8MA%3D%3D",
                    "https://images.unsplash.com/photo-1649521712353-e3661b4d42f4?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fG9mZmljZSUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D",
                    "https://images.unsplash.com/photo-1685602728729-064ce8fbf2f7?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fG9mZmljZSUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D",
                    "https://images.unsplash.com/photo-1716703373229-b0e43de7dd5c?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fG9mZmljZXxlbnwwfHwwfHx8MA%3D%3D",
                    "https://media.istockphoto.com/id/1493229333/photo/industrial-style-open-plan-office-interior-with-tables-computers-and-yellow-office-chairs.webp?b=1&s=612x612&w=0&k=20&c=AkJet0CzEuLg23b2GNZW_BnSH1RiyoU-d2X_AdEJ60M=",
                    "https://images.unsplash.com/photo-1715593949273-09009558300a?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fG9mZmljZSUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D",
                    "https://plus.unsplash.com/premium_photo-1670315267667-69a0b41d8384?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8b2ZmaWNlJTIwaW50ZXJpb3J8ZW58MHx8MHx8fDA%3D",
                    "https://images.unsplash.com/photo-1595846936289-91371459c5bd?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG9mZmljZSUyMGludGVyaW9yfGVufDB8fDB8fHww",
                    "https://images.unsplash.com/photo-1715593949345-50d3304cff4b?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjZ8fG9mZmljZSUyMGludGVyaW9yfGVufDB8fDB8fHww"
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