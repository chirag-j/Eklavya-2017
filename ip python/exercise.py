import cv2
import numpy as np
drawing = False
def nothing(x):
    pass
img = np.zeros((512,512,3))
cv2.namedWindow('image')

cv2.namedWindow('image')

def draw_circle(event,x,y,flags,param):
    global drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.circle(img,(x,y),ra,(b,g,r),-1)
    elif event ==  cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img,(x,y),ra,(b,g,r),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)
cv2.createTrackbar('RADIUS','image',0,255,nothing)
cv2.setMouseCallback('image',draw_circle)

while True:
    r=cv2.getTrackbarPos('R','image')
    g=cv2.getTrackbarPos('G','image')
    b=cv2.getTrackbarPos('B','image')
    ra=cv2.getTrackbarPos('RADIUS','image')
    cv2.imshow('image',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows
