from repo import create_book, create_review
import random

def seed_database():
    # Sample data
    books = [
        {"title": "1984", "author": "George Orwell"},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"title": "Pride and Prejudice", "author": "Jane Austen"},
        {"title": "The Catcher in the Rye", "author": "J.D. Salinger"}
    ]
    
    # Create books and store their IDs
    book_ids = []
    for book in books:
        result = create_book(title=book["title"], author=book["author"])
        if not hasattr(result, 'error'):
            book_ids.append(result.id)
            print(f"Created book: {result.title}")
        else:
            print(f"Error creating book: {result.error}")

    # Sample comments for variety
    comments = [
        "Absolutely loved it!",
        "A masterpiece.",
        "Couldn't put it down.",
        "Interesting perspective.",
        "Well written but not my style.",
        "Would recommend to others.",
        "Changed my perspective on life.",
        "A classic for good reason."
    ]

    # Create reviews for each book
    for book_id in book_ids:
        # Create 2-4 reviews per book
        num_reviews = random.randint(2, 4)
        for _ in range(num_reviews):
            rating = random.randint(1, 5)
            comment = random.choice(comments)
            result = create_review(rating=rating, comment=comment, book_id=book_id)
            if not hasattr(result, 'error'):
                print(f"Created review for book {book_id}: Rating {rating}")
            else:
                print(f"Error creating review: {result.error}")

if __name__ == "__main__":
    print("Starting database seeding...")
    seed_database()
    print("Database seeding completed!")
