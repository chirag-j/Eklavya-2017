import numpy as np
import cv2
cap = cv2.VideoCapture(0)

drawing = False
def draw_rect(event,x,y,flags,param):
    global drawing, ixr, iyr, jxr, jyr
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing1 = True
        drawing = True
        iyr, ixr = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img = cv2.rectangle(frame, (iyr,ixr), (x,y), (255,0,0), 2)
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img = cv2.rectangle(frame, (iyr,ixr), (x,y), (255,0,0), 2)
        jyr, jxr = x, y
        
#frame = np.zeros((512,512,3), np.uint8)
#cv2.namedWindow('frame')
_,frame = cap.read()
while True: 
    #cv2.imshow('frame', frame)
    cv2.setMouseCallback('red', draw_rect)
    cv2.imshow('red', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
#######################################################################################################################
print ixr, iyr
print jxr, jyr
################################################################################################################3
drawing = False
def draw_rect1(event,x,y,flags,param):
    global drawing, ixg, iyg, jxg, jyg
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        iyg, ixg = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img = cv2.rectangle(frame, (iyg,ixg), (x,y), (255,0,0), 2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img = cv2.rectangle(frame, (iyg,ixg), (x,y), (255,0,0), 2)
        jyg, jxg = x, y
        
#frame = np.zeros((512,512,3), np.uint8)
#cv2.namedWindow('frame')
_,frame = cap.read()

while True:
    
    #cv2.imshow('frame', frame)
    cv2.setMouseCallback('green', draw_rect1)
    cv2.imshow('green', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
#######################################################################################################################
print ixg, iyg
print jxg, jyg

#########################################################################################################################################    
# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
#r,h,c,w = 200,140,270,125  # simply hardcoded the values
r1 = ixr
h1 = jxr - ixr
c1 = iyr
w1 = jyr - iyr
track_window_r = (c1,r1,w1,h1)
##########################
r2 = ixg
h2 = jxg - ixg
c2 = iyg
w2 = jyg - iyg
track_window_g = (c2,r2,w2,h2)


# set up the ROI for tracking
roi_r = frame[r1:r1+h1, c1:c1+w1]
hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_red = np.array([0,100,50])
upper_red = np.array([20, 255, 255])
mask_r = cv2.inRange(hsv_roi, lower_red, upper_red)

roi_hist_r = cv2.calcHist([hsv_roi],[0],mask_r,[256],[0,255])
cv2.normalize(roi_hist_r,roi_hist_r,0,255,cv2.NORM_MINMAX)
##########################################
# set up the ROI for tracking
roi_g = frame[r2:r2+h2, c2:c2+w2]
#hsv_roi_g =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_green = np.array([110,55,55])
upper_green = np.array([130, 255, 255])
mask_g = cv2.inRange(hsv_roi, lower_green, upper_green)
roi_hist_g = cv2.calcHist([hsv_roi],[0],mask_g,[256],[0,255])
cv2.normalize(roi_hist_g,roi_hist_g,0,255,cv2.NORM_MINMAX)
# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
while True:
    ret ,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst_r = cv2.calcBackProject([hsv],[0],roi_hist_r,[0,255],1)
    dst_g = cv2.calcBackProject([hsv],[0],roi_hist_g,[0,255],1)
    #mask_r = cv2.inRange(hsv_roi, lower_red, upper_red)
    #mask_g = cv2.inRange(hsv_roi, lower_green, upper_green)
    
    #cv2.imshow('dst', dst)
    # apply meanshift to get the new location
    ret, track_window_r = cv2.meanShift(dst_r, track_window_r, term_crit)
    ret, track_window_g = cv2.meanShift(dst_g, track_window_g, term_crit)
    # Draw it on image
    x1,y1,w1,h1 = track_window_r
    x2,y2,w2,h2 = track_window_g
    img2 = cv2.rectangle(frame, (x1,y1), (x1+w1,y1+h1), (0,0,255),2)
    img3 = cv2.rectangle(img2, (x2,y2), (x2+w2,y2+h2), (255, 0, 0),2)
    cv2.imshow("img3",img3)

    k = cv2.waitKey(60) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
