from db import BookModel, DatabaseError, ReviewModel, get_db
from sqlalchemy.exc import SQLAlchemyError


def create_book(title: str, author: str, related_book_ids: list[int] = None):
    try:
        with get_db() as db:
            new_book = BookModel(title=title, author=author, related_book_ids=related_book_ids)
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
def get_related_books(book_id: int):
    try:
        with get_db() as db:
            return db.query(BookModel).filter(BookModel.related_book_ids.contains(str(book_id))).all()
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to get related books: {str(e)}")

def create_review(rating: int, comment: str, book_id: int):
    try:
        with get_db() as db:
            new_review = ReviewModel(rating=rating, comment=comment, book_id=book_id)
            db.add(new_review)
            db.commit()
            db.refresh(new_review)
            return new_review
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to create review: {str(e)}")
# naively get all reviews for a book
# def get_reviews(book_id: int):
#     try:
#         with get_db() as db:
#             return db.query(ReviewModel).filter(ReviewModel.book_id == book_id).all()
#     except SQLAlchemyError as e:
#         return DatabaseError(f"Failed to get reviews: {str(e)}")
# optimized get all reviews for a book
async def get_reviews(book_ids: list[int]):
    try:
        with get_db() as db:
            reviews = db.query(ReviewModel).filter(ReviewModel.book_id.in_(book_ids)).all()
            # Create a dictionary mapping book_ids to their reviews
            review_map = {}
            for review in reviews:
                if review.book_id not in review_map:
                    review_map[review.book_id] = []
                review_map[review.book_id].append(review)
            
            # Return reviews for each requested book_id in order, with error if not found
            return [
                review_map.get(book_id, [DatabaseError(f"No reviews found for book {book_id}")])
                for book_id in book_ids
            ]
    except SQLAlchemyError as e:
        return [DatabaseError(f"Failed to get reviews: {str(e)}") for _ in book_ids]

def get_review(review_id: int):
    try:
        with get_db() as db:
            return db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    except SQLAlchemyError as e:
        return DatabaseError(f"Failed to get review: {str(e)}")

def update_review(review_id: int, rating: int, comment: str):
    try:
        with get_db() as db:
            review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
            if not review:
                return DatabaseError("Review not found")
            review.rating = rating
            review.comment = comment
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