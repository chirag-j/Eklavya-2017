import cv2
import numpy as np
import math
drawing = False
ux = []
uy = []
vx = []
vy = []
cap = cv2.VideoCapture(0)
i = 0

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
    global drawing, ix, iy, jx, jy, i, abx, aby, frame_hsv
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        #go = False
        #print go
        ix, iy = x, y
        ux.append(ix)
        uy.append(iy)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(frame, (ix,iy), (x,y), (255,0,0), -1)
            
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame, (ix,iy), (x,y), (255,0,0), -1)
        jx, jy = x, y
        vx.append(jx)
        vy.append(jy)
        i+=1

    elif event == cv2.EVENT_RBUTTONDOWN:
        abx, aby = x, y
        print ('abx : ', abx, '  aby: ', aby)
        print (frame_hsv[aby, abx])
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', draw_rect)
while True:
    if drawing == False:
        ret, frame = cap.read()
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1)  == 27:
        break
cv2.destroyAllWindows()
roi1 = frame_hsv[uy[0]:vy[0], ux[0]:vx[0]]
h, s, v = np.median(roi1[:,:,0]), np.median(roi1[:,:,1]), np.median(roi1[:,:,2])
lower_range = np.array([h-5, s-50, v-70])
higher_range = np.array([h+5, s+50, v+70])
print "lower_range : ", lower_range
print "higher_range : ", higher_range
while True:
    ret, frame = cap.read()
    frame_h = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_h, lower_range, higher_range)
    mask = open_by_reconstruction(mask, iterations = 3)
    circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=20,maxRadius=100)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
    _, c, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
    # print ("wc: ", wc)
##    M = cv2.moments(c[idc])
##    cx = int(M['m10']/M['m00'])
##    cy = int(M['m01']/M['m00'])
##    roi1 = frame[cy-(wc/2):cy+(wc/2), cx-(wc/2):cx+(wc/2)]
##    mask[cy-5:cy+5, cx-5:cx+5] = 155
    cv2.drawContours(frame, c, idc, (255, 0, 0), 2)
##    cv2.imshow('roi', roi1)
    cv2.imshow('img', frame)
    cv2.imshow('mask', mask)
    if cv2.waitKey(1)  == 27:
        break
cv2.destroyAllWindows()
cap.release()
    
        
