import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    a = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    b = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.imshow("normal", img)

    cv2.imshow("Gray", a)
    cv2.imshow("HSF", b)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()    
