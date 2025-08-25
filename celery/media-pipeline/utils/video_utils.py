import os
from moviepy import VideoFileClip


def encode_video(file_path):
    output_path = file_path.replace(
        'uploads', 'processed').replace('.', '_encoded.')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    clip = VideoFileClip(file_path)
    clip.write_videofile(output_path, codec="libx264",
                         audio_codec="aac", logger=None)
    return output_path
