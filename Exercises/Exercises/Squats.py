import mediapipe as mp
from Exercises.angle import calculate_angle

mp_pose = mp.solutions.pose

count = 0
stage = ""

def get_squat_feedback(hip_knee_angle_left, hip_knee_angle_right):
    feedback = ""
    if hip_knee_angle_left > 90 or hip_knee_angle_right > 90:
        feedback += "Lower your hips more! " + stage
    return feedback if feedback else "Great job! Your squat form looks good! " + stage

def is_squat_down(hip_knee_angle_left, hip_knee_angle_right):
    return hip_knee_angle_left < 90 and hip_knee_angle_right < 90

def is_squat_up(hip_knee_angle_left, hip_knee_angle_right):
    return hip_knee_angle_left > 150 and hip_knee_angle_right > 150

def analyze_squats(results):
    global count, stage
    
    landmarks = results.pose_landmarks.landmark
    hip_left = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    hip_right = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
    knee_left = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
    knee_right = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
    ankle_left = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
    ankle_right = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
    
    hip_knee_angle_left = calculate_angle(hip_left, knee_left, ankle_left)
    hip_knee_angle_right = calculate_angle(hip_right, knee_right, ankle_right)
    
    feedback = get_squat_feedback(hip_knee_angle_left, hip_knee_angle_right)
    
    if is_squat_down(hip_knee_angle_left, hip_knee_angle_right):
        stage = "down"
    elif is_squat_up(hip_knee_angle_left, hip_knee_angle_right):
        if stage == "down":
            stage = "up"
            count += 1
    
    return feedback, count
