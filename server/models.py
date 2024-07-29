from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from config import db, bcrypt
##Users














##Spaces
class Space(db.Model, SerializerMixin):
    __tablename__ ='spaces'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tenant = db.relationship('User', back_populates = 'spaces')

    def __repr__(self):
        return f'<Space {self.title}, {self.description}>'
 










#Bookings




















#Reviews












#Payments