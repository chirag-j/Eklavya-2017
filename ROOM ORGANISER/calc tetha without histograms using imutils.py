import cv2
import numpy as np
import math
import time
from imutils.video import WebcamVideoStream

drawing = False
ux = []
uy = []
vx = []
vy = []
cap = WebcamVideoStream(src = 0).start()
ir = 0
abx = 0
aby = 0
def shift_origin(x,y):
    y = 480 - y
    return x,y

def calc_slope(x,y):
    cx1, cy1 = x
    cx2, cy2 = y
    tt1 = math.degrees(math.atan((cy2-cy1)/float(cx2-cx1)))
    if cx2<cx1 and cy2<cy1:
        tt1 = np.float32(math.degrees(-math.pi + math.atan((cy2-cy1)/float(cx2-cx1))))
    if cx2<cx1 and cy2>cy1:
        tt1 = np.float32(math.degrees(math.pi + math.atan((cy2-cy1)/float(cx2-cx1))))
    return tt1

def calc_tetha(tt1, tt2):
    if tt1>=0 and tt2>=0:
        if tt2>tt1:
            tetha = -(tt2 - tt1)
        else:
            tetha = tt1 - tt2
    elif tt1>=0 and tt2<0:
        if (tt1 + abs(tt2)) > 180:
            tetha = -(360 -(tt1 + abs(tt2)))
        else:
            tetha = tt1 + abs(tt2)

    elif tt1<0 and tt2>=0:
        
        if (tt2 + abs(tt1)) < 180:
            tetha = -(tt2 + abs(tt1))
        else :
            tetha = 360-(tt2 + abs(tt1))
    elif tt1<0 and tt2<0:
        if abs(tt2)<abs(tt1):
            tetha = -(abs(tt1) - abs(tt2))
        else :
            tetha = abs(tt2) - abs(tt1)
    return tetha

def open_by_reconstruction(src, iterations = 2, ksize = 3):
    
    eroded = cv2.erode(src, np.ones((ksize,ksize), np.uint8), iterations=iterations)
    this_iteration = eroded
    last_iteration = eroded
    while (True):
        this_iteration = cv2.dilate(last_iteration, np.ones((ksize,ksize), np.uint8), iterations = 1)
        this_iteration = this_iteration & src
        
        if np.array_equal(last_iteration, this_iteration):
            break
        last_iteration = this_iteration.copy()
       
    return this_iteration

def draw_rect(event,x,y,flags,param):
    global drawing, ix, iy, jx, jy, ir, abx, aby, frame_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        #go = False
        #print go
        ix, iy = x, y
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(frame, (ix,iy), (x,y), (255,0,0), -1)
            
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame, (ix,iy), (x,y), (255,0,0), -1)
        
        jx, jy = x, y
        if abs(jx-ix)>10 and abs(jy-iy)>10:
            ux.append(ix)
            uy.append(iy)
            vx.append(jx)
            vy.append(jy)
            ir+=1
        else:
            print "Rectangle was too small"

    elif event == cv2.EVENT_RBUTTONDOWN:
        abx, aby = x, y
        print 'abx : ', abx, '  aby: ', aby
        print frame_hsv[aby, abx]
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', draw_rect)
while True:
    if drawing == False:
        frame = cap.read()
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1)  == 27:
        if ir>=2:
            if abx!=0 and aby!=0:
                break
            else:
                print "Please Select a point by Right clicking anywhere on the screen"
        else:
            print "Please Select Atleast Two Rectangles"
            
cv2.destroyAllWindows()
print ir
roi = []
h = []
s = []
v = []
lower_range = []
upper_range = []
for var in range(0,ir):
    roi.append(frame_hsv[uy[var]:vy[var], ux[var]:vx[var]])
    h.append(np.median(roi[var][:,:,0]))
    s.append(np.median(roi[var][:,:,1]))
    v.append(np.median(roi[var][:,:,2]))
    lower_range.append(np.array([h[var]-5, s[var]-50, v[var]-70]))
    upper_range.append(np.array([h[var]+5, s[var]+50, v[var]+70]))
mask = np.zeros([ir, 480, 640], np.uint8)
cx = np.zeros([ir], np.uint32)
cy = np.zeros([ir], np.uint32)


while True:
    frame = cap.read()
    frame_h = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for ls in range(0,ir):
        mask[ls] = cv2.inRange(frame_h, lower_range[ls], upper_range[ls])
        mask[ls] = open_by_reconstruction(mask[ls])
        i, c, h = cv2.findContours(mask[ls], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(c)>0:
            max_area = 0
            counter = 0
            for n in c:
                a = cv2.contourArea(n)
                if a>max_area:
                    max_area = a
                    idc = counter
                counter+=1
            
            wc = math.sqrt(max_area)
            wc = int(1.5 * wc)
            M = cv2.moments(c[idc])
            cx[ls] = int(M['m10']/M['m00'])
            cy[ls] = int(M['m01']/M['m00'])
##            roi2 = frame[abs(int(cy-(wc/2))):cy+(wc/2), abs(int(cx-(wc/2))):cx+(wc/2)]
            mask[ls][cy[ls]-5:cy[ls]+5, cx[ls]-5:cx[ls]+5] = 155
            cv2.drawContours(frame, c, idc, (255, 0, 0), 2)
        else:
            print "obj no", ir, " not found"
            
    cv2.line(frame, (cx[0], cy[0]), (cx[1],cy[1]), (0,255,0), 1)
    cv2.line(frame, ( abx, aby) , (cx[1],cy[1]), (0,255,0), 1)
    cx0, cy0 = shift_origin(cx[0], cy[0])
    cx1, cy1 = shift_origin(cx[1], cy[1])
    abxs, abys = shift_origin(abx, aby)

    if cx[1]!=cx[0] and cx[1]!=abx:
        slope_bot = calc_slope((cx1, cy1),(cx0, cy0))
        slope_t = calc_slope((cx1, cy1),(abxs, abys))
        print "slope bot :", slope_bot
        print "slope target :", slope_t
        tetha = calc_tetha(slope_bot, slope_t)
        print "tetha : ",tetha


    
    mask_bot = mask[0] + mask[1]
    cv2.imshow('img', frame)
    cv2.imshow('mask', mask_bot)
    print time.time()
    if cv2.waitKey(1)  == 27:
        break

cv2.destroyAllWindows()
cap.release()
    
        
