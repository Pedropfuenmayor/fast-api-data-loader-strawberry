import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from repo import (
    create_book,
    create_review,
    delete_book,
    delete_review,
    get_book,
    get_books,
    get_reviews,
    update_book,
    update_review,
)


@strawberry.type
class Review:
    rating: int
    comment: str
    id: int


@strawberry.type
class Book:
    title: str
    author: str

    @strawberry.field
    def reviews(self) -> list[Review]:
        # Naively load reviews
        return get_reviews(self.id)

    id: int


@strawberry.type
class Query:
    books: list[Book] = strawberry.field(resolver=get_books)
    book: Book = strawberry.field(resolver=get_book)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        return create_book(title, author)

    @strawberry.mutation
    def update_book(self, book_id: int, title: str, author: str) -> Book:
        return update_book(book_id, title, author)

    @strawberry.mutation
    def delete_book(self, book_id: int) -> bool:
        return delete_book(book_id)

    @strawberry.mutation
    def add_review(self, rating: int, comment: str, book_id: int) -> Review:
        return create_review(rating, comment, book_id)

    @strawberry.mutation
    def update_review(self, review_id: int, rating: int, comment: str) -> Review:
        return update_review(review_id, rating, comment)

    @strawberry.mutation
    def delete_review(self, review_id: int) -> bool:
        return delete_review(review_id)


schema: strawberry.Schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app: GraphQLRouter = GraphQLRouter(
    schema=schema,
)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")