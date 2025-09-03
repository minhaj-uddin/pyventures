import os
import requests
import hashlib
import logging
from app import app

logger = logging.getLogger(__name__)

# Retry + acks_late setup
RETRY_KWARGS = {
    'autoretry_for': (Exception,),
    'retry_kwargs': {'max_retries': 3, 'countdown': 5},
    'acks_late': True
}


@app.task(name='video.http_chunk_download', **RETRY_KWARGS)
def http_chunk_download(start, end, chunk_number, url, output_dir):
    headers = {
        'Range': f'bytes={start}-{end - 1}',
        'User-Agent': 'ChunkedDownloader/1.0'
    }

    try:
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()

        os.makedirs(output_dir, exist_ok=True)
        chunk_path = os.path.join(output_dir, f'chunk_{chunk_number}.part')

        hasher = hashlib.sha256()

        with open(chunk_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    hasher.update(chunk)

        checksum = hasher.hexdigest()
        print(
            f"✅ Downloaded chunk {chunk_number} [{start}-{end}) — SHA256: {checksum}")

        return {
            "chunk_number": chunk_number,
            "chunk_path": chunk_path,
            "checksum": checksum
        }

    except Exception as e:
        logger.exception(f"❌ Failed to download chunk {chunk_number}: {e}")
        raise


@app.task(name='video.merge_chunks')
def merge_chunks(chunk_results, output_file="downloaded_video.mp4"):
    try:
        print("🔧 Merging chunks...")

        # Sort chunks by chunk_number
        sorted_chunks = sorted(chunk_results, key=lambda x: x['chunk_number'])

        with open(output_file, 'wb') as outfile:
            for result in sorted_chunks:
                with open(result['chunk_path'], 'rb') as infile:
                    outfile.write(infile.read())

        print(f"✅ File reassembled: {output_file}")
        return output_file

    except Exception as e:
        logger.exception("❌ Merge failed.")
        raise
