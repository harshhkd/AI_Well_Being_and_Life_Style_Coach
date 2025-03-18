import mediapipe as mp
from Exercises.angle import calculate_angle

mp_pose = mp.solutions.pose

count = 0
stage = ""

def get_pushup_feedback(elbow_angle_left, elbow_angle_right, shoulder_distance):
    feedback = ""
    
    if shoulder_distance < 0.1:
        feedback += "Keep your body straight! " + stage
    if elbow_angle_left > 90 or elbow_angle_right > 90:
        feedback += "Bend your elbows more to reach 90 degrees! " + stage
    
    return feedback if feedback else "Good job! Your form looks great!" + stage

def is_pushup_down(elbow_angle_left, elbow_angle_right):
    return elbow_angle_left < 90 and elbow_angle_right < 90

def is_pushup_up(elbow_angle_left, elbow_angle_right):
    return elbow_angle_left > 150 and elbow_angle_right > 150

def analyze_pushup(results):
    global count, stage
    
    landmarks = results.pose_landmarks
    shoulder_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    shoulder_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    elbow_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
    elbow_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
    wrist_left = landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    wrist_right = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
    
    shoulder_distance = abs(shoulder_left.x - shoulder_right.x)
    elbow_angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)
    elbow_angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)
    
    feedback = get_pushup_feedback(elbow_angle_left, elbow_angle_right, shoulder_distance)
    
    if is_pushup_down(elbow_angle_left, elbow_angle_right):
        stage = "down"
    elif is_pushup_up(elbow_angle_left, elbow_angle_right):
        if stage == "down":
            stage = "up"
            count += 1
    
    return feedback, count
