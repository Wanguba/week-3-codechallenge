
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create an engine
engine = create_engine('sqlite:///customers_table.sqlite')

Base = declarative_base()

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Float)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    # Define the relationship with Customer
    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', back_populates='customer')

    def get_reviews(self):
        return self.reviews

    def restaurants(self):
        return [review.restaurant for review in self.reviews]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        if not self.reviews:
            return None
        return max(self.reviews, key=lambda review: review.star_rating).restaurant

    def add_review(self, restaurant, rating):
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        self.reviews.append(new_review)

    def delete_reviews(self, restaurant):
        for review in self.reviews:
            if review.restaurant == restaurant:
                self.reviews.remove(review)

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define the relationship with Review
    reviews = relationship('Review', back_populates='restaurant')

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create instances and add them to the session

customer_instance = Customer(first_name='John', last_name='Lee')
restaurant_instance = Restaurant(name='Nairobi Street Kitchen')
review_instance = Review(star_rating=4.5, customer=customer_instance, restaurant=restaurant_instance)

customer_instance2 = Customer(first_name='Billy', last_name='Jean')
restaurant_instance2 = Restaurant(name='KFC')
review_instance = Review(star_rating=4, customer=customer_instance, restaurant=restaurant_instance)

customer_instance3 = Customer(first_name='Jean', last_name='Pierre')
restaurant_instance3 = Restaurant(name='Marcados')
review_instance = Review(star_rating=5, customer=customer_instance, restaurant=restaurant_instance)

# Add instances
session.add_all([customer_instance, restaurant_instance, review_instance])
session.add_all([customer_instance2, restaurant_instance2, review_instance])
session.add_all([customer_instance3, restaurant_instance3, review_instance])

# Commit the changes to the database
session.commit()


customers = session.query(Customer).all()
for customer in customers:
    print(f"Customer: {customer.full_name()}, Reviews: {len(customer.get_reviews())}")

restaurants = session.query(Restaurant).all()
for restaurant in restaurants:
    print(f"Restaurant: {restaurant.name}, Reviews: {len(restaurant.reviews)}")


