from aiohttp import web

# Size of the chunks to read
CHUNK_SIZE = 1024 * 1024  # 1MB


async def handle_upload(request):
    filename = request.headers.get('X-Filename', 'uploaded_file')
    dest_path = f'/uploads/{filename}'

    # Open a file in write-binary mode
    with open(dest_path, 'wb') as f:
        # Read incoming data in chunks
        async for chunk in request.content.iter_chunked(CHUNK_SIZE):
            if not chunk:
                break
            f.write(chunk)

    return web.Response(text=f"File {filename} uploaded successfully!")

# Create the aiohttp web app
app = web.Application()
app.router.add_post('/upload', handle_upload)

# Run the app
if __name__ == '__main__':
    web.run_app(app, port=8080)
