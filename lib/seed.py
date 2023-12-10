from your_models_module import Customer, Restaurant, Review, session

# Creating instances
customer1 = Customer(first_name='Billy', last_name='Jean')
customer2 = Customer(first_name='Ken', last_name='Carson')

restaurant1 = Restaurant(name='KFC', price=4000)
restaurant2 = Restaurant(name='Nairobi Street Kitchen', price=2500)

review1 = Review(customer=customer1, restaurant=restaurant1, star_rating=5)
review2 = Review(customer=customer2, restaurant=restaurant1, star_rating=4)
review3 = Review(customer=customer1, restaurant=restaurant2, star_rating=3)
review3 = Review(customer=customer2, restaurant=restaurant2, star_rating=4)

# Adding instances to the session and commit
session.add_all([customer1, customer2, restaurant1, restaurant2, review1, review2, review3])
session.commit()
