from celery import chain
from etl_tasks import extract_movies, transform_movies, load_movies

if __name__ == '__main__':
    api_url = 'https://playground.mockoon.com/movies'

    result = chain(
        extract_movies.s(api_url),
        transform_movies.s(),
        load_movies.s()
    )()

    print("Pipeline initiated. Task ID:", result.id)
    print(result.get())
