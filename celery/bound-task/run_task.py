from celery_app import app
from tasks import fetch_weather_data

print(f"Broker URL: {app.conf.broker_url}")
print(f"Registered tasks: {app.tasks.keys()}")

# Trigger the task
fetch_weather_data.delay("Islamabad")
