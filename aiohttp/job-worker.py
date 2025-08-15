import logging
import aiohttp
from aiohttp import web
from aiojobs.aiohttp import setup, spawn
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DOWNLOAD_DIR = Path("./downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)


# --- Background task function ---
async def download_file(url: str, filename: str) -> None:
    file_path = DOWNLOAD_DIR / filename

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.error(
                        f"Failed to download {url}: status {resp.status}")
                    return

                logger.info(f"Downloading {url} to {file_path}")
                with open(file_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(1024):
                        f.write(chunk)

        logger.info(f"Download completed: {file_path}")

    except Exception as e:
        logger.exception(f"Error while downloading {url}: {e}")


# --- aiohttp handler ---
async def start_download(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        url = data.get("url")

        if not url:
            return web.json_response({"error": "Missing 'url'"}, status=400)

        # Derive filename safely from URL
        filename = url.split("/")[-1] or "downloaded_file"

        # Spawn background task
        await spawn(request, download_file(url, filename))

        return web.json_response({"Status": "Download started", "filename": filename})

    except Exception as e:
        logger.exception("Failed to start download")
        return web.json_response({"error": str(e)}, status=500)


# --- App setup ---
def create_app() -> web.Application:
    app = web.Application()
    setup(app)  # Enable aiojobs scheduler
    app.router.add_post("/download", start_download)
    app.router.add_static("/", ".", show_index=True)
    return app


# --- Main entrypoint ---
if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="127.0.0.1", port=8080)
