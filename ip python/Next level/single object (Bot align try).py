import numpy as np
import cv2

cap = cv2.VideoCapture(0)
drawing = False
ret, frame = cap.read()
go = True
a, b = frame.shape[:2]

def draw_rect(event,x,y,flags,param):
    global drawing, ix, iy, jx, jy, go
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
roi = frame[ix:jx, iy:jy]
cv2.imshow('roi', roi)
##hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
##lower_red = np.array([0,150,50])
##upper_red = np.array([20, 255, 255])
##mask_red = cv2.inRange(hsv, lower_red, upper_red)
##cv2.imshow('red', mask_red)
##lower_blue = np.array([110,55,55])
##upper_blue = np.array([130, 255, 255])
##mask_blue = cv2.inRange(hsv, lower_red, upper_red)    
##cv2.imshow('blue', mask_blue)

_, img = cap.read()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = np.zeros([a, b], np.uint8)
mask[ix:jx, iy:jy] = [255]

hist = cv2.calcHist([hsv], [0, 1], mask, [180, 256], [0, 180, 0, 256])

cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
dst = cv2.calcBackProject([hsv],[0,1],hist,[0,180,0,256],1)
#cv2.imshow("dst1", dst)
#disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
#cv2.filter2D(dst,-1,disc,dst)
#ret,thresh = cv2.threshold(dst,50,255,0)
#thresh = cv2.merge((thresh,thresh,thresh))
#res = cv2.bitwise_and(img,thresh)
#cv2.imshow("res", res)
#cv2.imshow("img", img)
    
# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
#r,h,c,w = 200,140,270,125  # simply hardcoded the values
r = ix
h = jx - ix
c = iy
w = jy - iy
track_window = (c,r,w,h)

term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret ,frame = cap.read()
    roi = frame[ix:jx, iy:jy]
    cv2.imshow('roi', roi)
    
    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0, 1],hist,[0,180, 0, 255],1)
        cv2.imshow('dst', dst)
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        #pts = cv2.boxPoints(ret)
        #pts = np.int0(pts)
        #img2 = cv2.polylines(frame,[pts],True, 255,2)
        x,y,w,h = track_window
        img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cv2.imshow('img2',img2)


        
        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        
    else:
        break

cv2.destroyAllWindows()
cap.release()
