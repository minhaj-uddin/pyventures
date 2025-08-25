from celery_app import main
from utils.image_utils import resize_image, generate_thumbnail, apply_filters_and_watermark


@main.task
def process_image_task(file_path):
    resized_path = resize_image(file_path)
    generate_thumbnail(resized_path)
    apply_filters_and_watermark(resized_path)
    return f"Image processed: {resized_path}"
