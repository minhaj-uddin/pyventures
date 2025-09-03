from celery.schedules import crontab

# Optional: Save beat schedule to disk
beat_schedule_filename = 'beat_schedule.yaml'

beat_schedule = {
    'send-daily-digest-email': {
        'task': 'tasks.send_daily_digest',
        'schedule': crontab(hour=8, minute=0),
    },
}

# General Scheduling Settings
beat_schedule_filename = beat_schedule_filename
timezone = 'UTC'
