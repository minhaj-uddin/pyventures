# Run Celery worker and beat in parallel
celery -A app worker --loglevel=info --pool=solo &
celery -A app beat --loglevel=info --scheduler celery.beat:PersistentScheduler --schedule=beat_schedule.yaml
