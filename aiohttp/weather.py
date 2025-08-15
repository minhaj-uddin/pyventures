from aiohttp import web, ClientSession


async def get_weather(city):
    async with ClientSession() as session:
        url = f"https://wttr.in/{city}?format=3"
        async with session.get(url) as resp:
            return await resp.text()


async def weather_handler(request):
    city = request.rel_url.query.get('city', 'London')
    weather = await get_weather(city)
    return web.Response(text=f"Weather in {city}: {weather}")

app = web.Application()
app.router.add_get('/weather', weather_handler)

web.run_app(app, port=8080)
