from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Customer, Restaurant, Review

# Create an engine
engine = create_engine('sqlite:///database.sqlite')

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create instances and add them to the session

customer_instance = Customer(first_name='John', last_name='Lee')
restaurant_instance = Restaurant(name='Nairobi Street Kitchen', price=25.0)  # Add the price when creating the restaurant
review_instance = Review(star_rating=4.5, customer=customer_instance, restaurant=restaurant_instance)

customer_instance2 = Customer(first_name='Billy', last_name='Jean')
restaurant_instance2 = Restaurant(name='KFC', price=20.0)  # Add the price when creating the restaurant
review_instance2 = Review(star_rating=4, customer=customer_instance2, restaurant=restaurant_instance2)

customer_instance3 = Customer(first_name='Jean', last_name='Pierre')
restaurant_instance3 = Restaurant(name='Marcados', price=30.0)  # Add the price when creating the restaurant
review_instance3 = Review(star_rating=5, customer=customer_instance3, restaurant=restaurant_instance3)

# Add instances
session.add_all([customer_instance, restaurant_instance, review_instance])
session.add_all([customer_instance2, restaurant_instance2, review_instance2])
session.add_all([customer_instance3, restaurant_instance3, review_instance3])

# Commit the changes to the database
session.commit()

new_customer = Customer(first_name='Alice', last_name='Smith')

session.add(new_customer)

# Add a new review for the customer
Customer.add_review(restaurant=Restaurant, rating=3.5)
session.commit()

# Delete reviews for a specific restaurant
Customer.delete_reviews(restaurant=Restaurant)
session.commit()