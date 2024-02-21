from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import base64
import numpy as np
import os
import cv2

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Directory to save received frames
SAVE_DIR = 'received_frames'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

client_sockets = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    client_sockets[request.sid] = True

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    client_sockets.pop(request.sid, None)

@socketio.on('send_frame')
def handle_send_frame(frame_data):
    try:
        print('get Image')
        print(frame_data)
        # Step 2: Decode the received frame data
        frame_bytes = base64.b64decode(frame_data)

        # Step 3: Perform any additional processing if needed (e.g., convert to OpenCV image)
        frame = cv2.imdecode(np.frombuffer(frame_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Step 4: Save the frame as an image file
        save_path = os.path.join(SAVE_DIR, f'received_frame_{len(os.listdir(SAVE_DIR)) + 1}.jpg')

        # Save the image using cv2.imwrite with proper encoding
        success = cv2.imwrite(save_path, frame)

        if not success:
            raise ValueError("Failed to save the frame as an image.")

        # Step 6: Emit the frame back to the specific client for display
        emit('display_frame', {'frame': frame.tolist()}, room=request.sid)

        # Step 5: Emit the result to the client (optional)
        emit('fruit_result', {'result': 'Frame received on the server'})

    except Exception as e:
        print("Error during frame processing:", str(e))




@app.route('/')
def index():
    return render_template('index.html')


# Example log statements
print("Server starting...")
if __name__ == '__main__':
    socketio.run(app, debug=True)
