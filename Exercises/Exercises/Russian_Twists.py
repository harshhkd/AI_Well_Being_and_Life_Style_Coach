import mediapipe as mp
from Exercises.angle import calculate_angle

mp_pose = mp.solutions.pose

count = 0
current_side = None

def get_russian_twists_feedback(torso_angle_left, torso_angle_right):
    if torso_angle_left < 45 or torso_angle_right < 45:
        return "Twist your torso more to engage the obliques! "
    return "Great job! Your Russian twists form is good!"

def is_torso_twisted_left(torso_angle_left):
    return torso_angle_left > 45

def is_torso_twisted_right(torso_angle_right):
    return torso_angle_right > 45

def analyze_russian_twists(results):
    global count, current_side
    
    landmarks = results.pose_landmarks
    shoulder_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    shoulder_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    hip_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
    hip_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
    knee_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
    knee_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
    
    torso_angle_left = calculate_angle(hip_left, shoulder_left, knee_left)
    torso_angle_right = calculate_angle(hip_right, shoulder_right, knee_right)
    
    feedback = get_russian_twists_feedback(torso_angle_left, torso_angle_right)
    
    if is_torso_twisted_left(torso_angle_left) and current_side != 'left':
        current_side = 'left'
    elif is_torso_twisted_right(torso_angle_right) and current_side != 'right':
        current_side = 'right'
        if current_side == 'left':
            count += 1
    
    return feedback, count
