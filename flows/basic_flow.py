from prefect import flow


@flow
def my_favorite_function() -> int:
    print("This function doesn't do much")
    return 42
