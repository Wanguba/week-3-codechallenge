from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create an engine
engine = create_engine('sqlite:///restaurants_table.sqlite')

Base = declarative_base()

Base.metadata.bind = engine

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', back_populates='customer')

class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

    reviews = relationship('Review', back_populates='restaurant')

    def get_reviews(self):
        return self.reviews

    def get_customers(self):
        return [review.customer for review in self.reviews]

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Float)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')

# Create instances
customer_instance = Customer(first_name='John', last_name='Benson')
restaurant_instance = Restaurant(name='Nairobi Street Kitchen', price=50.0)
review_instance = Review(star_rating=4.5, customer=customer_instance, restaurant=restaurant_instance)

customer_instance1 = Customer(first_name='Kyle', last_name='Lowry')
restaurant_instance1 = Restaurant(name='KFC', price=35.0)
review_instance1 = Review(star_rating= 4.0, customer=customer_instance1, restaurant=restaurant_instance1)

# Add instances to the session
session.add_all([customer_instance, restaurant_instance, review_instance])
session.commit()

# Retrieve Restaurant instance
restaurant_instance = session.query(Restaurant).filter_by(id=1).first()

# Collection of reviews for the restaurant
reviews_collection = restaurant_instance.get_reviews()

# Collection of customers who reviewed the restaurant
customers_collection = restaurant_instance.get_customers()

# Printing results
print("Reviews for the restaurant:")
for review in reviews_collection:
    print(f"Review ID: {review.id}, Star Rating: {review.star_rating}")

print("\nCustomers who reviewed the restaurant:")
for customer in customers_collection:
    print(f"Customer ID: {customer.id}, Name: {customer.first_name} {customer.last_name}")
