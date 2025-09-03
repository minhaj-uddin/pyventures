import random
import requests
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=5)
def fetch_weather_data(self, city):
    url = f"https://api.weatherapi.com/v1/current.json"
    params = {
        "key": "YOUR_API_KEY",
        "q": city
    }

    try:
        logger.info(f"[{self.request.id}] Fetching weather data for: {city}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        logger.info(
            f"[{self.request.id}] Successfully fetched data for {city}: {data['current']['temp_c']}°C")
        return data

    except (Exception, AttributeError, ConnectionRefusedError,
            requests.exceptions.RequestException) as exc:
        retry_count = self.request.retries + 1
        max_retries = self.max_retries

        # Exponential backoff with jitter (2^retry_count + random 0-3 seconds)
        countdown = 2 ** retry_count + random.randint(0, 3)

        logger.warning(
            f"[{self.request.id}] Error fetching weather data for {city}. "
            f"Attempt {retry_count}/{max_retries}. Retrying in {countdown}s. Error: {str(exc)}"
        )

        raise self.retry(exc=exc, countdown=countdown)
