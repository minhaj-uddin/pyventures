import asyncio
import aiohttp


async def send_file():
    data = aiohttp.FormData()
    data.add_field('file',
                   open('example.txt', 'rb'),
                   filename='example.txt',
                   content_type='text/plain')

    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8080/upload', data=data) as resp:
            print(f'Status: {resp.status}')
            print('Response:', await resp.text())

# Run the async function
asyncio.run(send_file())
