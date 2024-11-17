from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import Session 

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

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_book(db: Session, title: str, author: str):
    new_book = BookModel(title=title, author=author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def update_book(db: Session, book_id: int, title: str, author: str):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if book:
        book.title = title
        book.author = author
        db.commit()
        db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    return False

def get_book(db: Session, book_id: int):
    return db.query(BookModel).filter(BookModel.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BookModel).offset(skip).limit(limit).all()

def create_review(db: Session, rating: int, title: str, book_id: int):
    new_review = ReviewModel(rating=rating, title=title, book_id=book_id)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def get_reviews(db: Session, book_id: int):
    return db.query(ReviewModel).filter(ReviewModel.book_id == book_id).all()

def get_review(db: Session, review_id: int):
    return db.query(ReviewModel).filter(ReviewModel.id == review_id).first()    

def update_review(db: Session, review_id: int, rating: int, title: str):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if review:
        review.rating = rating
        review.title = title
        db.commit()
        db.refresh(review)
    return review

def delete_review(db: Session, review_id: int):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if review:
        db.delete(review)
        db.commit()
        return True
    return False



