import numpy as np
import cv2

cap = cv2.VideoCapture(0)
drawing = False
#go = True
_, frame = cap.read()
i = 0
obj_lim = 10
ux = np.zeros([obj_lim], np.uint8)
vx = np.zeros([obj_lim], np.uint8)
uy = np.zeros([obj_lim], np.uint8)
vy = np.zeros([obj_lim], np.uint8)
a, b = frame.shape[:2]
print a,b

def draw_rect(event,x,y,flags,param):
    global drawing, ix, iy, jx, jy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        #go = False
        #print go
        iy, ix = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(frame, (iy,ix), (x,y), (255,0,0), -1)
            jy, jx = x, y
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame, (iy,ix), (x,y), (255,0,0), -1)
        #go = True
        
        
#frame = np.zeros((512,512,3), np.uint8)
#cv2.namedWindow('frame')
ret,frame = cap.read()

while True:
    
    
    if drawing == False:
        ret, frame = cap.read()
       
    
    cv2.setMouseCallback('frame', draw_rect)
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('n'):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        
        
        ux[i], uy[i], vx[i], vy[i] = ix, iy, jx, jy
        print ux[i], vx[i], uy[i], vy[i]
        print i
        i+=1
        
        
    elif k == 27:
        break
    
cv2.destroyAllWindows()
#######################################################################################################################
print ux
_, img = cap.read()
a, b = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = np.zeros([a, b], np.uint8)

for n in range(0,i):
    mask[ux[n]:vx[n], uy[n]:vy[n]] = [255]
cv2.imshow('mask', mask)
while True:
    k = cv2.waitKey(60) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()
    
    
    




