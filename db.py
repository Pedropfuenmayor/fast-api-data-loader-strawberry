from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

# Create PostgreSQL database engine
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/mydb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create declarative base class
Base = declarative_base()

# Define Book model
class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    reviews = relationship("ReviewModel", back_populates="book")

# Define Review model
class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    title = Column(String)
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("BookModel", back_populates="reviews")

# Create all tables
Base.metadata.create_all(bind=engine)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB 
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DatabaseError:
    def __init__(self, message: str):
        self.message = message

def create_book(title: str, author: str):
    try:
        with get_db() as db:
            new_book = BookModel(title=title, author=author)
            db.add(new_book)
            db.commit()
            db.refresh(new_book)
            return new_book
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to create book: {str(e)}")

def update_book(book_id: int, title: str, author: str):
    try:
        with get_db() as db:
            book = db.query(BookModel).filter(BookModel.id == book_id).first()
            if not book:
                return DatabaseError("Book not found")
            book.title = title
            book.author = author
            db.commit()
            db.refresh(book)
            return book
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to update book: {str(e)}")

def delete_book(book_id: int):
    try:
        with get_db() as db:
            book = db.query(BookModel).filter(BookModel.id == book_id).first()
            if not book:
                return DatabaseError("Book not found")
            db.delete(book)
            db.commit()
            return True
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to delete book: {str(e)}")
def get_book(book_id: int):
    try:
        with get_db() as db:
            return db.query(BookModel).filter(BookModel.id == book_id).first()
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to get book: {str(e)}")

def get_books(skip: int = 0, limit: int = 100):
    try:
        with get_db() as db:
            return db.query(BookModel).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to get books: {str(e)}")

def create_review(rating: int, title: str, book_id: int):
    try:
        with get_db() as db:
            new_review = ReviewModel(rating=rating, title=title, book_id=book_id)
            db.add(new_review)
            db.commit()
            db.refresh(new_review)
            return new_review
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to create review: {str(e)}")

def get_reviews(book_id: int):
    try:
        with get_db() as db:
            return db.query(ReviewModel).filter(ReviewModel.book_id == book_id).all()
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to get reviews: {str(e)}")

def get_review(review_id: int):
    try:
        with get_db() as db:
            return db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to get review: {str(e)}")

def update_review(review_id: int, rating: int, title: str):
    try:
        with get_db() as db:
            review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
            if not review:
                return DatabaseError("Review not found")
            review.rating = rating
            review.title = title
            db.commit()
            db.refresh(review)
            return review
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to update review: {str(e)}")

def delete_review(review_id: int):
    try:
        with get_db() as db:
            review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
            if not review:
                return DatabaseError("Review not found")
            db.delete(review)
            db.commit()
            return True
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to delete review: {str(e)}")



