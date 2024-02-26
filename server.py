import os
from flask import Flask, request, jsonify
import numpy as np
import cv2
import base64

app = Flask(__name__)

# Directory to save received frames
SAVE_DIR = 'received_frames'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Step 1: Receive the frame data from the request body
        frame_data = request.data
        print("Received frame data length:", len(frame_data))

        # Step 2: Decode the received frame data
        frame_bytes = base64.b64decode(frame_data)

        # Step 3: Convert frame data to numpy array
        frame_np = np.frombuffer(frame_bytes, dtype=np.uint8)
        print(frame_np)

        # Step 4: Decode the numpy array to an image
        frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)

        # Check if the frame is valid
        if frame is None:
            print("Invalid frame data received")
            return jsonify({'error': 'Invalid frame data'}), 400

        # Print frame dimensions
        print("Received frame dimensions:", frame.shape)

        # Step 5: Save the frame as an image file
        save_path = os.path.join(SAVE_DIR, f'received_frame_{len(os.listdir(SAVE_DIR)) + 1}.jpg')
        cv2.imwrite(save_path, frame)
        print("Frame saved to:", save_path)

        # Step 6: Respond with a success message
        return jsonify({'message': 'Frame received on the server'}), 200

    except Exception as e:
        print("Error during frame processing:", str(e))
        return jsonify({'error': 'Error processing frame'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
