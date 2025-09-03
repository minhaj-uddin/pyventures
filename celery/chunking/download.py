import os
import math
from celery import chord
from tasks import http_chunk_download, merge_chunks

CHUNK_SIZE = 1024 * 1024  # 1MB/Chunk


def get_remote_file_size(url):
    import requests
    response = requests.head(url, allow_redirects=True)
    response.raise_for_status()
    return int(response.headers.get('Content-Length'))


def create_download_args(url, output_dir):
    file_size = get_remote_file_size(url)
    print(f"🌐 Remote file size: {file_size} bytes")

    total_chunks = math.ceil(file_size / CHUNK_SIZE)
    args = []

    for i in range(total_chunks):
        start = i * CHUNK_SIZE
        end = min((i + 1) * CHUNK_SIZE, file_size)
        args.append((start, end, i, url, output_dir))

    return args


if __name__ == '__main__':
    output_dir = "downloadeds"
    output_file = os.path.join(output_dir, "downloaded_video.mp4")
    url = "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/1080/Big_Buck_Bunny_1080_10s_10MB.mp4"

    download_args = create_download_args(url, output_dir)

    # Use chord with chunk-style mapping
    chord_header = [http_chunk_download.s(*args) for args in download_args]
    final_step = merge_chunks.s(output_file)

    result = chord(chord_header)(final_step)

    print(f"🚀 Chunked download started. Chord ID: {result.id}")
