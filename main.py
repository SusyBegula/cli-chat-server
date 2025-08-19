# client.py - The Client
import asyncio
import websockets
import threading
import sys

# --- IMPORTANT: CHANGE THIS URL ---
# This will be the URL you get from Render in Step 4
SERVER_URL = "ws://your-chat-app.onrender.com/ws" 
# Note: Use wss:// if your server uses SSL (Render does)
# So it should be: "wss://your-chat-app.onrender.com/ws"


async def receive_messages(websocket):
    """Listens for incoming messages and prints them."""
    try:
        async for message in websocket:
            # Clears the current line and prints the message
            print("\r" + " " * 60, end="") # Clear line
            print(f"\rUnknown: {message}")
            print("You: ", end="", flush=True) # Reprint your prompt
    except websockets.exceptions.ConnectionClosed:
        print("\nConnection to server lost.")

def send_messages(websocket_uri):
    """Handles user input and sends it to the server."""
    # This part runs in the main thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def sender():
        async with websockets.connect(websocket_uri) as websocket:
            # Start the receiver task in the background
            receiver_task = asyncio.create_task(receive_messages(websocket))
            
            print("Connected to chat! Type your message and press Enter.")
            
            while True:
                # Get input from the user in a non-blocking way
                message = await loop.run_in_executor(None, sys.stdin.readline)
                message = message.strip()
                
                if message:
                    await websocket.send(message)
                # This gives the receiver a chance to run
                await asyncio.sleep(0.1)

    try:
        loop.run_until_complete(sender())
    except KeyboardInterrupt:
        print("\nExiting chat.")

if __name__ == "__main__":
    # Replace the URL with the wss one for Render
    secure_url = SERVER_URL.replace("ws://", "wss://")
    print("Connecting to chat server...")
    send_messages(secure_url)
