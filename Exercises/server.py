from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from main import estimate_pose
import time


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def process_frame_async(frame, mode):
    feedback, count = estimate_pose(frame, mode)
    return {"feedback": feedback, "count": count}

last_frame_time = 0

@app.route('/pose-correct', methods=['POST'])
def pose_correct():
    global last_frame_time
    try:
        mode = request.form.get('mode')
        frame = request.files.get('frame')

        if frame is None:
            return jsonify(error="No file uploaded"), 400

        file = np.frombuffer(frame.read(), np.uint8)
        frame = cv2.imdecode(file, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify(error="Invalid or corrupt image file"), 400

        current_time = time.time()
        if current_time - last_frame_time < 0.05:
            return jsonify(error="Frame skipped to maintain sync"), 429
        last_frame_time = current_time
        feedback, count = estimate_pose(frame, mode)
        return jsonify({"feedback": feedback, "count": count})

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)