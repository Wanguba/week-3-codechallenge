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
restaurant_instance = Restaurant(name='Nairobi Street Kitchen', price=25.0)
review_instance = Review(star_rating=4.5, customer=customer_instance, restaurant=restaurant_instance)

customer_instance2 = Customer(first_name='Billy', last_name='Jean')
restaurant_instance2 = Restaurant(name='KFC', price=20.0)
review_instance2 = Review(star_rating=4, customer=customer_instance2, restaurant=restaurant_instance2)

customer_instance3 = Customer(first_name='Jean', last_name='Pierre')
restaurant_instance3 = Restaurant(name='Marcados', price=30.0)
review_instance3 = Review(star_rating=5, customer=customer_instance3, restaurant=restaurant_instance3)

# Add instances
session.add_all([customer_instance, restaurant_instance, review_instance])
session.add_all([customer_instance2, restaurant_instance2, review_instance2])
session.add_all([customer_instance3, restaurant_instance3, review_instance3])

# Commit the changes to the database
session.commit()

# Add a new review for the customer
new_customer = Customer(first_name='Alice', last_name='Smith')
session.add(new_customer)
new_review = Review(star_rating=3.5, customer=new_customer, restaurant=restaurant_instance)
session.add(new_review)
session.commit()

# Delete reviews for a specific restaurant
restaurant_to_delete_reviews = Restaurant(name='KFC', price=20.0)
customer_to_delete_reviews = Customer(first_name='Billy', last_name='Jean')

# Assuming you know the specific instances of restaurant and customer for which you want to delete reviews
customer_to_delete_reviews.delete_reviews(session, restaurant_to_delete_reviews)
session.commit()

# Query and print the results
customers = session.query(Customer).all()
for customer in customers:
    print(f"Customer: {customer.full_name()}, Reviews: {len(customer.reviews)}")

restaurants = session.query(Restaurant).all()
for restaurant in restaurants:
    print(f"Restaurant: {restaurant.name}, Price: {restaurant.price}, Reviews: {len(restaurant.reviews)}")

# Fanciest restaurant
restaurant = Restaurant.fanciest(session)
print(f"The fanciest restaurant is: {restaurant.name} with price {restaurant.price}")

reviews = restaurant.all_reviews()
for review in reviews:
    print(review)
