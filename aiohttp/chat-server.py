import sockjs
from aiohttp import web

# Store active sessions
sessions = set()


async def chat_handler(manager, session, msg):
    if msg.tp == sockjs.MsgType.OPEN:
        sessions.add(session)
        print(f"Client connected: {session.id}")
        return

    elif msg.tp == sockjs.MsgType.CLOSE:
        sessions.discard(session)
        print(f"Client disconnected: {session.id}")
        return

    elif msg.tp == sockjs.MsgType.MESSAGE:
        text = msg.data
        print(f"Received message: {text}")

        # Broadcast to all clients
        for s in sessions.copy():
            if s != session:
                s.send(f"{session.id[:5]}: {text}")

# Create aiohttp app
app = web.Application()

# Register SockJS endpoint
sockjs.add_endpoint(app, chat_handler, name='chat', prefix='/chat')


async def index(request):
    return web.Response(text=HTML_PAGE, content_type='text/html')

app.router.add_get("/", index)

# HTML + SockJS frontend
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>SockJS Chat</title>
    <script src="https://cdn.jsdelivr.net/npm/sockjs-client@1/dist/sockjs.min.js"></script>
</head>
<body>
    <h2>Simple SockJS Chat</h2>
    <div id="chat" style="height: 200px; border: 1px solid #ccc; overflow-y: scroll;"></div>
    <input id="input" autocomplete="off" placeholder="Type message..." />
    <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('input');

        const sock = new SockJS('/chat');

        sock.onmessage = function(e) {
            const msg = document.createElement('div');
            msg.textContent = e.data;
            chat.appendChild(msg);
            chat.scrollTop = chat.scrollHeight;
        };

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                sock.send(input.value);
                input.value = '';
            }
        });
    </script>
</body>
</html>
"""

# Run the app
if __name__ == '__main__':
    web.run_app(app, port=8080)
