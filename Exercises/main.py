import cv2
import mediapipe as mp
from Exercises.Push_Ups import analyze_pushup
from Exercises.Pull_Ups import analyze_pullup
from Exercises.Squats import analyze_squats
from Exercises.Jumping_Jacks import analyze_jumping_jacks
from Exercises.Russian_Twists import analyze_russian_twists
from mediapipe.python.solutions.pose import Pose

mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()
pose = mp_pose.Pose(static_image_mode=False,
                     model_complexity=1,
                     smooth_landmarks=True,
                     min_detection_confidence=0.5,
                     min_tracking_confidence=0.5)


def reset_pose():
    global pose
    pose.close()  # Close existing Pose instance
    pose = Pose()

#
# def estimate_pose(frame, mode):
#     feedback, count = "No pose detected", 0
#     try:
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(frame_rgb)
#
#         if results.pose_landmarks:
#             if mode == 'push':
#                 feedback, count = analyze_pushup(results)
#             elif mode == 'pull':
#                 feedback, count = analyze_pullup(results)
#             elif mode == 'squat':
#                 feedback, count = analyze_squats(results)
#             elif mode == 'jack':
#                 feedback, count = analyze_jumping_jacks(results)
#             elif mode == 'twist':
#                 feedback, count = analyze_russian_twists(results)
#             else:
#                 feedback = "Invalid mode specified"
#     except Exception as e:
#         feedback = f"Error: {str(e)}"
#     return feedback, count


import collections

# Store last feedback and count persistently
feedback_buffer = collections.deque(maxlen=5)
persistent_count = {"push": 0, "pull": 0, "squat": 0, "jack": 0, "twist": 0}

def estimate_pose(frame, mode):
    global feedback_buffer, persistent_count
    feedback, count = "No pose detected", persistent_count.get(mode, 0)

    try:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            if mode == 'push':
                feedback, count = analyze_pushup(results)
            elif mode == 'pull':
                feedback, count = analyze_pullup(results)
            elif mode == 'squat':
                feedback, count = analyze_squats(results)
            elif mode == 'jack':
                feedback, count = analyze_jumping_jacks(results)
            elif mode == 'twist':
                feedback, count = analyze_russian_twists(results)
            else:
                feedback = "Invalid mode specified"

            # Update persistent count only when valid pose is detected
            persistent_count[mode] = count

        # Store last few feedbacks
        feedback_buffer.append(feedback)

        # Use most common feedback
        stable_feedback = max(set(feedback_buffer), key=feedback_buffer.count)

    except Exception as e:
        stable_feedback = f"Error: {str(e)}"

    return stable_feedback, persistent_count.get(mode, 0)

