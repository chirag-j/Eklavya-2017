import cv2
import numpy as np
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
while True:
    
    if ret == True:
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord('q'):
            ret = False
            print ret
    else:
        print 'out'
        break
    
cv2.destroyAllWindows()
print ret
    
