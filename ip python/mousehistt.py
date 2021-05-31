import numpy as np
import cv2

cap = cv2.VideoCapture(0)
drawing = False

cap_ = True
def draw_rect(event,x,y,flags,param):
    global drawing, ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(frame, (ix,iy), (x,y), (255,0,0), 2)
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame, (ix,iy), (x,y), (255,0,0), 2)
        
#frame = np.zeros((512,512,3), np.uint8)
#cv2.namedWindow('frame')

while True:
    if drawing == False:
        _,frame = cap.read()
        
    #cv2.imshow('frame', frame)
    
        
  
    cv2.setMouseCallback('frame', draw_rect)
    cv2.imshow('frame', frame)
    
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()
    
    
