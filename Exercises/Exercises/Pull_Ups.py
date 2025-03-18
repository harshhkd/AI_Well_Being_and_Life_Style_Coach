import mediapipe as mp
from Exercises.angle import calculate_angle

mp_pose = mp.solutions.pose

count = 0
stage = ""

def get_pullup_feedback(elbow_angle_left, elbow_angle_right, shoulder_distance, hip_position, shoulder_y):
    feedback = ""
    
    if shoulder_distance < 0.1:
        feedback += "Keep your body straight! "
    if elbow_angle_left < 90 and elbow_angle_right < 90:
        feedback += "Your elbows are in the right position! "
    else:
        feedback += "Bend your elbows more to pull up! "
    if hip_position < shoulder_y:
        feedback += "Keep your hips up during the pull-up! "
    
    return feedback if feedback else "Great work! Your form looks good!"

def is_pulled_up(elbow_angle_left, elbow_angle_right):
    return elbow_angle_left < 90 and elbow_angle_right < 90

def is_hanging(elbow_angle_left, elbow_angle_right):
    return elbow_angle_left > 150 and elbow_angle_right > 150

def analyze_pullup(results):
    global count, stage
    
    landmarks = results.pose_landmarks
    shoulder_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    shoulder_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    elbow_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
    elbow_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
    wrist_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    wrist_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
    hip_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
    hip_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
    
    elbow_angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)
    elbow_angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)
    shoulder_distance = abs(shoulder_left.x - shoulder_right.x)
    hip_position = (hip_left.y + hip_right.y) / 2
    shoulder_y = min(shoulder_left.y, shoulder_right.y)
    
    feedback = get_pullup_feedback(elbow_angle_left, elbow_angle_right, shoulder_distance, hip_position, shoulder_y)
    
    if is_pulled_up(elbow_angle_left, elbow_angle_right):
        stage = "up"
    elif is_hanging(elbow_angle_left, elbow_angle_right):
        if stage == "up":
            stage = "down"
            count += 1
    
    return feedback, count