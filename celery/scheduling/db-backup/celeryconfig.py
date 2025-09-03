from celery.schedules import crontab

beat_schedule = {
    'daily-db-backup': {
        'task': 'tasks.backup_database',
        'schedule': crontab(hour=2, minute=0)
    },
}

timezone = 'UTC'
