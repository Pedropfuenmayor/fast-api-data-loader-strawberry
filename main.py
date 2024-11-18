import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.dataloader import DataLoader

from repo import create_book, create_review, delete_book, delete_review, get_book, get_books, get_related_books, get_review, get_reviews, update_book, update_review

loader = DataLoader(load_fn=get_reviews)


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
        # naively load reviews for now
        # return get_reviews(self.id)
        # optimized 
        return loader.load(self.id)
    id: int

@strawberry.type
class Query:
    books: list[Book] = strawberry.field(resolver=get_books)
    book: Book = strawberry.field(resolver=get_book)
    # reviews: list[Review] = strawberry.field(resolver=get_reviews)
    review: Review = strawberry.field(resolver=get_review)


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
