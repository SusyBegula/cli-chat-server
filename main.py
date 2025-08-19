# main.py - The Server
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

# Create the FastAPI app instance
app = FastAPI()

# A list to keep track of all active WebSocket connections
connections: List[WebSocket] = []

# This is the main endpoint for your chat
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the new client connection
    await websocket.accept()
    connections.append(websocket)
    print(f"New client connected. Total clients: {len(connections)}")
    
    try:
        # Loop forever, waiting for messages from this client
        while True:
            # Wait for a message
            data = await websocket.receive_text()
            
            # Broadcast the received message to all other clients
            for connection in connections:
                if connection != websocket: # Don't send the message back to the sender
                    await connection.send_text(data)
    except WebSocketDisconnect:
        # If a client disconnects, remove them from the list
        connections.remove(websocket)
        print(f"Client disconnected. Total clients: {len(connections)}")
