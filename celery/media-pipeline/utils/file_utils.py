import os
import shutil


def save_upload(src_path, dest_dir='uploads'):
    os.makedirs(dest_dir, exist_ok=True)
    filename = os.path.basename(src_path)
    dest_path = os.path.join(dest_dir, filename)
    shutil.copy(src_path, dest_path)
    return dest_path


def is_image(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))


def is_video(filename):
    return filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
