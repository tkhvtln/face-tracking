import cv2
import dlib
import math
from face_detection import detect_face
from math_utils import compute_transform_params
from video_utils import input_video, resize_and_transform, progress_bar


cap = cv2.VideoCapture()
cap = input_video(cap)
save = input('Enter the path and filename to save the output (e.g., C:/path/to/output.avi): ')

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(save, fourcc, 30.0, (width, height))

fps = cap.get(cv2.CAP_PROP_FPS)
lengthVideo = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
durationVideo = math.trunc(float(lengthVideo) / float(fps))
print('\nDuration:\t', durationVideo, 'sec', '\nScreen : \t', width, 'x', height, '\n')

print('Loading...')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')

frameCount  = 0

while True:
    ret, frame = cap.read()
    
    if ret == True:
        tx, ty, cx, cy, wx, hy  = detect_face(frame, detector, predictor)
        angle, scale, translation_matrix, rotate_matrix = compute_transform_params(frame, tx, ty, cx, cy, wx, hy, width, height)
        frame = resize_and_transform(frame, width, height, scale, translation_matrix, rotate_matrix, tx, ty)
        
        out.write(frame)
        cv2.imshow('Frame', frame)

        frameCount += 1
        progress_bar(frameCount, lengthVideo)

        if cv2.waitKey(1) == ord('q') :
            print('\n\nBreak')
            break

    else:
        print('\n\nFinish')
        break

cap.release()
out.release()
cv2.destroyAllWindows()
