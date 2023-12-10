
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from your_database_module import Base, session

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

    # Define the relationship with Review
    reviews = relationship('Review', back_populates='restaurant')

    # Include the methods for Restaurant class from the provided code
    def reviews(self):
        return self.reviews

    def customers(self):
        return [review.customer for review in self.reviews]

    @classmethod
    def fanciest(cls):
        return max(session.query(cls).all(), key=lambda restaurant: restaurant.price)

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

# Import the Review class if it's in a separate file
from your_database_module import Review
