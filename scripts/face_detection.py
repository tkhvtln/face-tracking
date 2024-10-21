import cv2


def detect_face(frame, detector, predictor):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    faces = detector(gray)
    tx, ty, cx, cy, wx, hy = 0, 0, 0, 0, 0, 0
        
    for face in faces:
        landmarks = predictor(gray, face)

        tx = landmarks.part(28).x - frame.shape[1] / 2
        ty = landmarks.part(28).y - frame.shape[0] / 2
                
        cx = landmarks.part(30).x - landmarks.part(29).x
        cy = landmarks.part(30).y - landmarks.part(29).y
            
        wx = face.right() - face.left()
        hy = face.bottom() - face.top()

    return tx, ty, cx, cy, wx, hy