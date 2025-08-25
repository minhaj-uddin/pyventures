from celery import Celery


main = Celery('media_pipeline',
              broker='redis://localhost:6379/0',
              backend='redis://localhost:6379/0',
              include=['tasks.image_tasks', 'tasks.video_tasks']
              )

main.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
)
