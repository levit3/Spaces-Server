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
        tenants = User.query.filter_by(role=UserRole.TENANT).all()
        for _ in range(50):
            tenant = choice(tenants)
            space = Space(
                title=fake.company(),
                description=fake.text(max_nb_chars=200),
                location=fake.city(),
                price_per_hour=randint(10, 300),
                status=rc(["available", "unavailable"], k=1)[0],
                tenant_id=tenant.id
            )
            spaces.append(space)
        db.session.add_all(spaces)
        db.session.commit()
        print(f"Space data seeded successfully. Total spaces: {len(spaces)}")
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
                    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGeI6be1l5nFx752kcU8y6jxtmsGugYvC7Cw&s",
                    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqxrzw3sRFwoMy2teoaO_oedw6-EbasiLEbQ&s",
                    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsv5BghQypAA9vL-F_dueyDaJmYiYCsfyZUA&s",
                    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0q1-ZXX1ueiy5mmfD8HkhEt6Sc_jNf4xeNg&s",
                    # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT27H5Kc3MuLwzQMvZdT76_yeiEgabghpwpSw&s",
                   "https://images.squarespace-cdn.com/content/v1/60da576b8b440e12699c9263/1665048935960-1W7UVYJZMYIW7E12Y8XW/ovation+2.jpg?format=750w"
"https://colony.work/wp-content/uploads/2019/12/Copy-of-StarBoulevard-56-min-1024x532.jpg"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRh_FpfaZod6mxUYoIs0Sxkk6oEAgSRk0om6g&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmnE8X4TZdIkh_HVRi_i4yPoB2l0KM3zKjUA&s"
"https://static.giggster.com/media/activities/event/uploads/1707915804/1080.jpg"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQo61vP5DcXRiZoHFRJmH5UkZvLVLzqENyDBA&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTebj9ulBRtsFODqQlnCe6WmSzKakQZbQl9Ig&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSY6sKcAWb2POxeT8GDSwBHkhjZhIXZCFL2uQNt69Taw-pxGJEP5lpDtgPhx3yYHXu6niw&usqp=CAU"
"https://i.pinimg.com/236x/95/02/87/950287796d3677e5536ff5f27877c678.jpg"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTqXSg56Pd5DQCyi5oNUKG7sV33R3cgB_xQpvOhiYx-nfBZ6BXdflfpg4IrFEgMZGHxydY&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4il5-VgA9t8pPTD2AUXzMDAWZRbGU2Kh0i4z3ar0tlwqeOWzHvVY-N27eSLRFS1bnz_c&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIDMdm05eQ3T4EjXIkcX5573D9eYvAg_PjjQ&s"
"https://images.squarespace-cdn.com/content/v1/60da576b8b440e12699c9263/1650354559198-U58EM4C8OL0QIVOW3CSN/Ovation.jpg"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZMY4E-5DmO4yulFIekO9Ilrf1vBYf7R_c66J1KoMj73kJYJcweNHog9e2fy1o6xJ5c0I&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSW8VAflmx42lhhUBIzjBWvOUDzviG2zYRKVZKHbzqaABQ7ZJ-YQGMoLK0mwepIBUJTtYY&usqp=CAU"
"https://img.bizbash.com/files/base/bizbash/bzb/image/2012/04/aria___convention_center___bristlecone_ballroom___wide_event.png?auto=format%2Ccompress&q=70&w=400"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQdngbAcxHPQG9xjY5-vuqWEX5ceAADTZ60Sg&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0kc7OTULccvzkIN288emNDXcke6uDrJjHVthntyFWzkln0dYwn7B7O_UDNDnX29p_cMY&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT1lXiKDVNg3PYbmpWQA-ivmcZj_C_Y32Q-aQ&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZOw5HslBizPHqPsNNwjNtouJylqYImCE2-KdUoNYZ7344AJqRfZpjh8CN5Ez2iBa3-WI&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZng24ctxztlZJxz4L12mecBfRGMGpbweJESpTW8LsFn7eQBwSqZqK8fGBPWhyigZqH8c&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_wKS8ZcLhi5qek5p1C9w_b23eKkxUd9maI-C-FKqUS-J_WfQ4B8T3hpI-9xR5UXgujZg&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxIGmQQUrMJAtlJNUHjS3oMTWTNckYizQbZA&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDkSSIxFDlybZOw3p5KuEBRbs5IiSTCEkjyQ&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNdSUZNI1Epjrn9NELZe_xPHfiKYDGRmZ-8FXSkAGcSxR_wSLvyHIR_1qw9EREPGfGJXk&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1hmJl_ImtTf7hBUxmPncuz8Kq9yRAeBeC1Q&s"
"https://memo.thevendry.com/wp-content/uploads/2022/06/Glasshouse-chelsea-1.jpg"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScmNe-j2wxijK_cWnK_Xqwnx8Y9vzzJxiCloGj4BNGZBI91RIB7_0HnLyg39l0Kb18wkc&usqp=CAU"
"https://i0.wp.com/eventspacesny.com/wp-content/uploads/2023/03/2.jpg?fit=1150%2C765&ssl=1"
"https://www.bizzabo.com/wp-content/uploads/2021/09/21_20100309113817_196133_large.jpg"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQo-iKCc-1BNxDvIyihDYnTBQmkIPM5DLLhv5CR-oGZUM6j0yN9GZLPnL8QwgGeB-Hckh4&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTg43P81TcD3qjBhwRB-imqSqpii5hosZSKdmUbSE_bYWh-0bsuYKrxcCOG69zOpXCfPdI&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTL9aIq5NMYqfYdlgIOIi6W4DT2iF3ad_upUC_ukJAQ1X5-tdh3r1kn22adWFkhxSmkspo&usqp=CAU"
"https://www.uottawa.ca/about-us/sites/g/files/bhrskd336/files/styles/max_width_l_1470px/public/2021-12/spaces-tbt112-wide-header1.jpg?itok=7lBAzQdZ"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRL8dyYft7S7vnbMBXIlYYM5SZdIBAMI1mg4gj5Qz7b8_pUN7TJqgAyIFmoJTOCTxnO6z4&usqp=CAU"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmWTfecKWKYK9Yb8k1eso98hyrTWLtAgUlRA&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQG4THSD8aoNrTSTKljZXCon4k-DSRAjn9vOg&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDFQdhXO0Rv-qzejfvoRhYSqo2R5pcUH4yLw&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNzZu8V6hcKuFuajew4hWmbesSOE21OYPoTg&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVscy8aegxYCJWvgDo_tzrSytvR2SiN9267w&s"
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2TvNJsoYz89tj8aS-yLiIe2JfGge9_abpxQ&s"

                     ]

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
