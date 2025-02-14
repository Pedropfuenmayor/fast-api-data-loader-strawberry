# Data loader implementation with Fast API and Strawberry.

## What problem does data loader solve?

Data loader is a utility that solve the n+1 problem in Graphql.

### What is the n+1 problem?

The n+1 occurs when we make an initial request, fallowed by some unknown number of follow-up requests.

### What is a data loader?

> DataLoader is a generic utility to be used as part of your application's data fetching layer to provide a simplified and consistent API over various remote data sources such as databases or web services via batching and caching.

### Docs reference

- [Data loader](https://github.com/graphql/dataloader)
- [Strawberry Data Loader](https://strawberry.rocks/docs/guides/dataloaders#dataloaders)

## Local setup

### Tools

- Docker
- GNU make
- Poetry

### Commands

```sh

#Clone the repo
mkdir data-loader && cd data-loader

git clone https://github.com/Pedropfuenmayor/fast-api-data-loader-strawberry.git .

# Install dependencies and create a virtual environment
poetry install

# Activate the virtual environment.
poetry shell

# Start the database container
make db-up

# Run database migrations
make db-migrate

# Seed the database
make db-seed

# Start the development server
make dev

# Start the naive development server
make dev-naive
```

## Testing query results

**Fetch the books**

```gql
query {
  books {
    title
    id
    reviews {
      comment
    }
  }
}
```

I naive application make 5 roundtrips to the db for the review table. With the data loader utility we make one.

See the logs.

## Key implementations

### Custom context and data loader

- Custom context for a per request data loader initialization for providing request-scoped caching. After the request is processed, the context is destroyed and the loader is garbage collected, ensuring proper cleanup of cached data.

```python
class CustomContext(BaseContext):
    def __init__(self, reviews_loader: DataLoader):
        self.reviews_loader = reviews_loader


def custom_context_loader() -> CustomContext:
    reviews_loader = DataLoader(load_fn=get_reviews_batched)
    return CustomContext(reviews_loader=reviews_loader)


async def get_context(
    custom_context=Depends(custom_context_loader),
) -> CustomContext:
    return custom_context

    #...

    graphql_app: GraphQLRouter = GraphQLRouter(
    schema=schema,
    context_getter=get_context,
)

```

### Use the loader in the resolver

```python
@strawberry.type
class Book:
    title: str
    author: str

    @strawberry.field
    def reviews(self, info: strawberry.Info[CustomContext]) -> list[Review]:
        return info.context.reviews_loader.load(self.id)

    id: int
```

### Batching function

```python
async def get_reviews_batched(book_ids: list[int]):
    """
    Batch function implementation following DataLoader pattern:
    https://github.com/graphql/dataloader?tab=readme-ov-file#batch-function
    """
    try:
        with get_db() as db:
            reviews = db.query(ReviewModel).filter(ReviewModel.book_id.in_(book_ids)).all()
            review_map = {}
            for review in reviews:
                if review.book_id not in review_map:
                    review_map[review.book_id] = []
                review_map[review.book_id].append(review)
            return [
                review_map.get(book_id, [DatabaseError(f"No reviews found for book {book_id}")])
                for book_id in book_ids
            ]
    except SQLAlchemyError as e:
        return [DatabaseError(f"Failed to get reviews: {str(e)}") for _ in book_ids]
```
