import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from db import create_book, get_books


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

@strawberry.type
class Query:
    books: list[Book] = strawberry.field(resolver=get_books)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        return create_book(title, author)
        


schema: strawberry.Schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app: GraphQLRouter = GraphQLRouter(
    schema=schema,
)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
