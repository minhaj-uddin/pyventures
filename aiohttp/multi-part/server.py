import os
from aiohttp import web

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def handle_upload(request):
    reader = await request.multipart()
    field = await reader.next()

    while field is not None:
        if field.name == 'file':
            filename = field.filename
            save_path = os.path.join(UPLOAD_DIR, filename)

            with open(save_path, 'wb') as f:
                while True:
                    chunk = await field.read_chunk()
                    if not chunk:
                        break
                    f.write(chunk)
        field = await reader.next()

    return web.Response(text="File uploaded successfully!")

app = web.Application()
app.router.add_post('/upload', handle_upload)

if __name__ == '__main__':
    web.run_app(app, port=8080)
