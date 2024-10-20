import cv2
import dlib
import numpy
import math
    

def inputVido(cap):
    while not cap.isOpened():
        file = input('Enter the path to an .avi file: ')    
        cap = cv2.VideoCapture(file)
        
        if not cap.isOpened():
            print('File does not exist')

    return cap


def calculate(tx, ty, cx, cy, wx, hy):
    ab = (1, 0)
    cd = (cx, cy)
    scale = 1

    angle = 0 #int(-math.degrees(ab[0] * cd[0] + ab[1] * cd[1]) / (math.sqrt(ab[0] ** 2 + cd[0] ** 2) + math.sqrt(ab[1] ** 2 + cd[1] ** 2)))

    w, h = rotatedRectWithMaxArea(width, height, math.radians(angle))
    r = (100 - ((w * h * 100) / (width * height))) / 100

    s1 = width * height
    s2 = wx * hy

    if s1 != 0 and s2 != 0:
        scale = (100 - (s2 * 100 / s1)) / 100 + 1 
    

    rotate_matrix = cv2.getRotationMatrix2D((frame.shape[1] / 2, frame.shape[0] / 2), angle, 1)
    translation_matrix = numpy.float32([[1, 0, -tx], [0, 1, -ty]])

    return angle, scale, translation_matrix, rotate_matrix
    

def rotatedRectWithMaxArea(w, h, angle):
    if w <= 0 or h <= 0:
        return 0,0

    width_is_longer = w >= h
    side_long, side_short = (w, h) if width_is_longer else (h, w)

    sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
    if side_short <= 2. * sin_a * cos_a * side_long or abs(sin_a - cos_a) < 1e-10:     
        x = 0.5 * side_short
        wr, hr = (x / sin_a,x / cos_a) if width_is_longer else (x / cos_a, x / sin_a)
    else:
        cos_2a = cos_a * cos_a - sin_a * sin_a
        wr, hr = (w * cos_a - h * sin_a) / cos_2a, (h * cos_a - w * sin_a) / cos_2a

    return wr, hr


def detectFace(frame):
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


def showFrame(frame, scale, translation_matrix, rotate_matrix):
    frame = cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)), interpolation = cv2.INTER_AREA) #resize        
    if -(frame.shape[1] / 2 - width / 2) < tx < (frame.shape[1] / 2 - width / 2) and -(frame.shape[0] / 2 - height / 2) < ty < (frame.shape[0] / 2 - height / 2):
        frame = cv2.warpAffine(frame, translation_matrix, (frame.shape[1], frame.shape[0])) #transform

    frame = cv2.warpAffine(frame, rotate_matrix, (frame.shape[1], frame.shape[0])) #rotate        
    frame = frame[int(frame.shape[0] / 2 - height / 2) : int(frame.shape[0] / 2 + height / 2),
                  int(frame.shape[1] / 2 - width  / 2) : int(frame.shape[1] / 2 + width  / 2)] #cut

    return frame


def progressBar(current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end = '\r')



iFrame = 0
cap = cv2.VideoCapture()

cap = inputVido(cap)
save = input('Save as: ')

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
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    
while True:
    ret, frame = cap.read()
    
    if ret == True:
        tx, ty, cx, cy, wx, hy  = detectFace(frame)
        angle, scale, translation_matrix, rotate_matrix = calculate(tx, ty, cx, cy, wx, hy)
        frame = showFrame(frame, scale, translation_matrix, rotate_matrix)
        
        out.write(frame)
        cv2.imshow('Frame', frame)

        iFrame += 1
        progressBar(iFrame, lengthVideo)


        if cv2.waitKey(1) == ord('q') :
            print('\n\nBreak')
            break

    else:
        print('\n\nFinish')
        break

cap.release()
out.release()
cv2.destroyAllWindows()

input()
