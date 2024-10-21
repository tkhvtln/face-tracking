import cv2


def input_video(cap):
    while not cap.isOpened():
        file = input('Enter the path to an .avi file (e.g., C:/path/to/input.avi): ')    
        cap = cv2.VideoCapture(file)
        
        if not cap.isOpened():
            print('File does not exist')

    return cap


def resize_and_transform(frame, width, height, scale, translation_matrix, rotate_matrix, tx, ty):
    frame = cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)), interpolation = cv2.INTER_AREA) #resize        
    if -(frame.shape[1] / 2 - width / 2) < tx < (frame.shape[1] / 2 - width / 2) and -(frame.shape[0] / 2 - height / 2) < ty < (frame.shape[0] / 2 - height / 2):
         frame = cv2.warpAffine(frame, translation_matrix, (frame.shape[1], frame.shape[0])) #transform

    frame = cv2.warpAffine(frame, rotate_matrix, (frame.shape[1], frame.shape[0])) #rotate        
    frame = frame[int(frame.shape[0] / 2 - height / 2) : int(frame.shape[0] / 2 + height / 2),
                  int(frame.shape[1] / 2 - width  / 2) : int(frame.shape[1] / 2 + width  / 2)] #cut

    return frame


def progress_bar(current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end = '\r')