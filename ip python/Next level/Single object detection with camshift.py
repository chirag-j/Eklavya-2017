import numpy as np
import cv2

cap = cv2.VideoCapture(0)
drawing = False
_, img = cap.read()

a, b = img.shape[:2]

def open_by_reconstruction(src, iterations = 3, ksize = 3):
    
    # first erode the source image
    eroded = cv2.erode(src, np.ones((ksize,ksize), np.uint8), iterations=iterations)
 
    # Now we are going to iteratively regrow the eroded mask.
    # The key difference between just a simple opening is that we
    # mask the regrown everytime with the original src.
    # Thus, the dilated mask never extends beyond where it does in the original.
    
    this_iteration = eroded
    last_iteration = eroded
    while (True):
        this_iteration = cv2.dilate(last_iteration, np.ones((ksize,ksize), np.uint8), iterations = 1)
        this_iteration = this_iteration & src
        
        if np.array_equal(last_iteration, this_iteration):
            # convergence!
            break
        last_iteration = this_iteration.copy()
       
    return this_iteration

def draw_rect(event,x,y,flags,param):
    global drawing, ix, iy, jx, jy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing1 = True
        drawing = True
        iy, ix = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img = cv2.rectangle(frame, (iy,ix), (x,y), (255,0,0), 2)
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img = cv2.rectangle(frame, (iy,ix), (x,y), (255,0,0), 2)
        jy, jx = x, y
        
#frame = np.zeros((512,512,3), np.uint8)
#cv2.namedWindow('frame')
_,frame = cap.read()

while True:
    if drawing == False:
        ret, frame = cap.read()
    #cv2.imshow('frame', frame)
    cv2.setMouseCallback('frame', draw_rect)
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()
#######################################################################################################################
print ix, iy
print jx, jy



_, img = cap.read()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = np.zeros([a, b], np.uint8)
mask[ix:jx, iy:jy] = [255]

hist = cv2.calcHist([hsv], [0, 1], mask, [180, 256], [0, 180, 0, 256])

cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
dst = cv2.calcBackProject([hsv],[0,1],hist,[0,180,0,256],1)
##cv2.imshow("dst1", dst)
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cv2.filter2D(dst,-1,disc,dst)
ret,thresh = cv2.threshold(dst,50,255,0)
thresh = cv2.merge((thresh,thresh,thresh))
res = cv2.bitwise_and(img,thresh)
##cv2.imshow("res", res)
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

# set up the ROI for tracking
#roi = frame[r:r+h, c:c+w]
#hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#lower_red = np.array([0,150,150])
#upper_red = np.array([30, 255, 255])
#mask = cv2.inRange(hsv_roi, lower_red, upper_red)
#cv2.imshow('mask', mask)
#roi_hist = cv2.calcHist([hsv_roi],[0],mask,[256],[0,255])
#cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0, 1],hist,[0,180, 0, 255],1)
        #cv2.imshow('dst', dst)
        
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        cv2.filter2D(dst,-1,disc,dst)
        ret,thresh = cv2.threshold(dst,50,255,0)
        thresh = cv2.merge((thresh,thresh,thresh))
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # Draw it on image
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv2.polylines(frame,[pts],True, 255,2)
        cv2.imshow('img2',img2)
        cv2.imshow('dst',dst)
    
        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg",img2)

    else:
        break

cv2.destroyAllWindows()
cap.release()
    
    











