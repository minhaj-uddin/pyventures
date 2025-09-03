celery -A app worker --loglevel=info &
celery -A app beat --loglevel=info
