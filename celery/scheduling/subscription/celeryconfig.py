from celery.schedules import crontab

beat_schedule = {
    'hourly-subscription-check': {
        'task': 'tasks.process_due_subscriptions',
        'schedule': crontab(minute=0),
    },
}

timezone = 'UTC'
