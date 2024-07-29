##Users














##Spaces












#Bookings

class Booking(db.Model,SerializerMixin):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'))
    booking_id = db.Column(db.Integer,


















#Reviews












#Payments