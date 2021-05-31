import cv2
import numpy as np
def obj(event,x,y,flags,param):
    global drawing, ix, iy, jx, jy, i
    if event == cv2.EVENT_LBUTTONDBLCLK:
        drawing = True
        #go = False
        #print go
        iy, ix = x, y
    

img = cv2.imread('ÿ.jpg')

while True:
   
    
    cv2.setMouseCallback('img', obj)
    cv2.imshow('img', img)
    k = cv2.waitKey(1) & 0xFF  
    if k == 27:
        break
    
cv2.destroyAllWindows()
print ix,iy

