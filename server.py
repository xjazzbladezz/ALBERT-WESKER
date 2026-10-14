import asyncio
import http.server
import json
import random
import socketserver
import threading
import websockets

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def start_http_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"HTTP Local Server running at http://localhost:{PORT}")
        httpd.serve_forever()

async def ws_handler(websocket):
    print("Game client connected to Python RL engine!")
    try:
        async for message in websocket:
            data = json.loads(message)
            if data.get("event") == "player_shoot":
                selected_action = random.choice([1, 2]) if random.random() < 0.7 else random.choice([0, 3])
                response = {"action": selected_action}
                await websocket.send(json.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def start_ws_server():
    print("WebSocket RL Engine running at ws://localhost:8765")
    async with websockets.serve(ws_handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    threading.Thread(target=start_http_server, daemon=True).start()
    try:
        asyncio.run(start_ws_server())
    except KeyboardInterrupt:
        print("\nServer shut down.")
