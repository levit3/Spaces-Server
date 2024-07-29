from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from config import db, bcrypt
##Users














##Spaces
class Spaces(db.Model, SerializerMixin):
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
class Review(db.Model, SerializerMixin):
  __tablename__ = 'reviews'
  
  id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer, nullable=False)
  comment = db.Column(db.String(1000), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=False)
  date = db.Column(db.Date, server_default=func.current_date())
  
  @validates('rating')
  def validate_rating(self, key, rating):
    if not (5 >= int(rating) >= 0):
      raise ValueError('Rating must be between 1 and 5')
    return rating
  
  @validates('user_id')
  def validate_user_id(self, key, user_id):
    user = User.query.get(user_id).first()
    if not user:
      raise ValueError('User does not exist')
    return user_id
  
  @validates('space_id')
  def validate_space_id(self, key, space_id):
    space = Space.query.get(space_id).first()
    if not space:
      raise ValueError('Space does not exist')
    return space_id
  
  @validates('comment')
  def validate_comment(self, key, comment):
    if len(comment) < 5:
      raise ValueError('Comment must be at least 5 characters long')
    return comment
  








#Payments