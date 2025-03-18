import numpy as np

def calculate_angle(point1, point2, point3):
    a = np.array([point1.x,point1.y])
    b = np.array([point2.x,point2.y])
    c = np.array([point3.x,point3.y])
    
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)