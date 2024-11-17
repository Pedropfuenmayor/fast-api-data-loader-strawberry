import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Review:
    rating: int
    title: str
    id: int


@strawberry.type
class Book:
    title: str
    author: str
    reviews: list[Review]
    id: int

    # in memory list of books


books = [
    Book(
        title="Book 1",
        author="Author 1",
        reviews=[Review(rating=5, title="Great book", id=1)],
        id=1,
    ),
]


def get_books():
    return books


@strawberry.type
class Query:
    books: list[Book] = strawberry.field(resolver=get_books)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        book = Book(title=title, author=author, reviews=[], id=len(books) + 1)
        books.append(book)
        return book


schema: strawberry.Schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app: GraphQLRouter = GraphQLRouter(
    schema=schema,
)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
