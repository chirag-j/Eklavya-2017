import cv2
import numpy as np
cap = cv2.VideoCapture(1)
while(1):

    # Take each frame
    _, frame = cap.read()
    equ = cv2.equalizeHist(frame)
    res = np.hstack((frame,equ))
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
