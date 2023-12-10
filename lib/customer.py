
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from customers.py import Base, session

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key = True)
    first_name = Column(String)
    last_name = Column(String)

    # Define the relationship with Review
    reviews = relationship('Review', back_populates='customer')

    # Include the methods for Customer class from the provided code
    def reviews(self):
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

# Import the Review class if it's in a separate file
from customers.py import Review
