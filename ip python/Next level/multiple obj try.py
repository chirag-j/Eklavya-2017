import numpy as np
import cv2

cap = cv2.VideoCapture(0)
drawing = False
ret, frame = cap.read()
i = 0
obj_lim = 10
ux = np.zeros([obj_lim])
vx = np.zeros([obj_lim])
uy = np.zeros([obj_lim])
vy = np.zeros([obj_lim])
go = True
a, b = frame.shape[:2]

def draw_rect(event,x,y,flags,param):
    global drawing, ix, iy, jx, jy, go, i
    if event == cv2.EVENT_LBUTTONDOWN:
        go = False
        drawing = True
        iy, ix = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(frame, (iy,ix), (x,y), (255,0,0), -1)
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame, (iy,ix), (x,y), (255,0,0), -1)
        jy, jx = x, y
        ux[i], uy[i], vx[i], vy[i] = ix, iy, jx, jy
        print ux[i], uy[i], vx[i], vy[i]
        print i
        i+=1
        
#frame = np.zeros((512,512,3), np.uint8)
#cv2.namedWindow('frame')
ret,frame = cap.read()

while True:
    if go == True:
        ret,frame = cap.read()
    cv2.setMouseCallback('frame', draw_rect)
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
#######################################################################################################################
print ix, iy
print jx, jy
