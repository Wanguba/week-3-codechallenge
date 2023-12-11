from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Create an engine
engine = create_engine('sqlite:///database.sqlite')

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', back_populates='customer')

    def customer_reviews(self, session):  
        return session.query(Review).filter_by(customer_id=self.id).all()

    def customer_restaurants(self, session):  
        return session.query(Restaurant).join(Review).filter(Review.customer_id == self.id).all()

    def full_name(self):  
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else "Unknown Name"

    def favorite_restaurant(self, session):  
        reviews_list = self.customer_reviews(session)
        favorite_review = max(reviews_list, key=lambda review: review.star_rating, default=None)
        return favorite_review.restaurant if favorite_review else None

    def add_review(self, session, restaurant, rating):  
        if restaurant and rating is not None:
            new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
            session.add(new_review)
            session.commit()

    def delete_reviews(self, session, restaurant):  
        if restaurant:
            session.query(Review).filter_by(customer_id=self.id, restaurant_id=restaurant.id).delete()
            session.commit()

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Float)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

    reviews = relationship('Review', back_populates='restaurant')

    @classmethod
    def fanciest(cls, session):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        review_strings = []

        for review in self.reviews:
            customer_name = review.customer.full_name() if review.customer else "Unknown Customer"
            review_string = f"Review for {self.name} by {customer_name}: {review.star_rating} stars."
            review_strings.append(review_string)

        return review_strings
    
# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Commit the changes to the database
session.commit()

# Query and print the results
customers = session.query(Customer).all()
for customer in customers:
    print(f"Customer: {customer.full_name()}, Reviews: {len(customer.reviews)}")

restaurants = session.query(Restaurant).all()
for restaurant in restaurants:
    print(f"Restaurant: {restaurant.name}, Price: {restaurant.price}, Reviews: {len(restaurant.reviews)}")

# Close the session when done
session.close()



