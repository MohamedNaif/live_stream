import os
import cv2
from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

def generate_frames():
    cap = cv2.VideoCapture(0)  # 0 for default camera (laptop camera)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to capture frame")
            break
        # (Optional) Apply image processing here

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_as_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_as_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
