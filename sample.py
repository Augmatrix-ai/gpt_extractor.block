from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive a message

            # Send a response or stream data back
            response = f"Message processed"
            await websocket.send_text(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
