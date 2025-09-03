import requests
from celery_app import app
from collections import defaultdict


@app.task(name='etl.extract_movies')
def extract_movies(api_url: str) -> list:
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()


@app.task(name='etl.transform_movies')
def transform_movies(movies: list) -> dict:
    grouped = defaultdict(list)
    for m in movies:
        year = m.get('releaseYear')
        grouped[year].append(m)
    # Sort each group by rating descending
    for year, group in grouped.items():
        group.sort(key=lambda x: x.get('rating', 0), reverse=True)
    return dict(grouped)


@app.task(name='etl.load_movies')
def load_movies(grouped_movies: dict) -> str:
    for year in sorted(grouped_movies):
        print(f"=== {year} ===")
        for movie in grouped_movies[year]:
            print(f"{movie.get('rating', '?')}/10 — {movie.get('title')}")
    return f"Processed {len(grouped_movies)} movies."
