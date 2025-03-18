import mediapipe as mp
from Exercises.angle import calculate_angle

mp_pose = mp.solutions.pose

count = 0
is_open = False

def get_jumping_jacks_feedback(shoulder_angle_left, shoulder_angle_right, leg_distance):
    feedback = ""
    if shoulder_angle_left > 150 and shoulder_angle_right > 150:
        feedback += "Raise your arms fully! "
    if leg_distance < 0.1:
        feedback += "Jump wider with your legs! "
    return feedback if feedback else "Your jumping jack looks good!"

def is_jumping_jacks_open(shoulder_angle_left, shoulder_angle_right, leg_distance):
    return shoulder_angle_left > 150 and shoulder_angle_right > 150 and leg_distance > 0.3

def is_jumping_jacks_closed(shoulder_angle_left, shoulder_angle_right, leg_distance):
    return shoulder_angle_left < 90 and shoulder_angle_right < 90 and leg_distance < 0.1

def analyze_jumping_jacks(results):
    global count, is_open
    
    landmarks = results.pose_landmarks
    shoulder_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    shoulder_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    elbow_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
    elbow_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
    hip_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
    hip_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
    knee_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
    knee_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
    
    shoulder_angle_left = calculate_angle(hip_left, shoulder_left, elbow_left)
    shoulder_angle_right = calculate_angle(hip_right, shoulder_right, elbow_right)
    leg_distance = abs(knee_left.x - knee_right.x)
    
    feedback = get_jumping_jacks_feedback(shoulder_angle_left, shoulder_angle_right, leg_distance)
    
    if is_jumping_jacks_open(shoulder_angle_left, shoulder_angle_right, leg_distance) and not is_open:
        is_open = True
    elif is_jumping_jacks_closed(shoulder_angle_left, shoulder_angle_right, leg_distance) and is_open:
        is_open = False
        count += 1
    
    return feedback, count
