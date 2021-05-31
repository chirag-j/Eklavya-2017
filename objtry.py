import cv2
import numpy as np
def obj(event,x,y,flags,param):
    global drawing, ix, iy, jx, jy, i
    if event == cv2.EVENT_LBUTTONDBCLK:
        drawing = True
        #go = False
        #print go
        iy, ix = x, y
    
ret,frame = cap.read()

while True:
    ret,frame = cap.read()
    
    cv2.setMouseCallback('frame', obj)
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xFF  
    if k == 27:
        break
    
cv2.destroyAllWindows()
print ix,iy
