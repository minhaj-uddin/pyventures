import sys
from utils.file_utils import save_upload, is_image, is_video
from tasks.image_tasks import process_image_task
from tasks.video_tasks import process_video_task


def main(file_path):
    uploaded_path = save_upload(file_path)
    print(f"Uploaded: {uploaded_path}")

    if is_image(uploaded_path):
        print("Dispatching image processing task...")
        process_image_task.delay(uploaded_path)
    elif is_video(uploaded_path):
        print("Dispatching video processing task...")
        process_video_task.delay(uploaded_path)
    else:
        print("Unsupported file type.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
    else:
        main(sys.argv[1])
