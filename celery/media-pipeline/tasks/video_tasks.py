from celery_app import main
from utils.video_utils import encode_video


@main.task
def process_video_task(file_path):
    output_path = encode_video(file_path)
    return f"Video encoded: {output_path}"
