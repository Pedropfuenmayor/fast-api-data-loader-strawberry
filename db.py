from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/mydb"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base = declarative_base()
class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    reviews = relationship("ReviewModel", back_populates="book")

class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    comment = Column(String)
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("BookModel", back_populates="reviews")

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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





