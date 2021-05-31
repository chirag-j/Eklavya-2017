import numpy as np
import cv2
import math
import httplib
IP_addr1 = "192.168.0.102"
cap = cv2.VideoCapture(0)
flag = True
flag1 = True
drawing = False
#go = True
ret, frame = cap.read()
i = 0
obj_lim = 10
ux = np.zeros([obj_lim], np.uint32)
vx = np.zeros([obj_lim], np.uint32)
uy = np.zeros([obj_lim], np.uint32)
vy = np.zeros([obj_lim], np.uint32)
point = ( 86 , 302 )

def line_track(tetha):
    
    data = 'f'
    if tetha>10 or tetha<-10:
        if tetha>10 and tetha<15:
            data = 'a'
        elif tetha>15 and tetha<20:
            data = 'a'
        elif tetha>20 and tetha<30:
            data = 'a'
        elif tetha>30:
            data = 'a'
            
        if tetha<-10 and tetha>-15:
            data = 'd'
        elif tetha<-15 and tetha>-20:
            data = 'd'
        elif tetha<-20 and tetha>-30:
            data = 'd'
        elif tetha<-30:
            data = 'd'
    print 'data: ', data
        
            
    
    

def calc_slope(x,y):
    cx1, cy1 = x
    cx2, cy2 = y
    tt1 = math.degrees(math.atan((cy2-cy1)/float(cx2-cx1)))
    if cx2<cx1 and cy2<cy1:
        tt1 = math.degrees(-math.pi + math.atan((cy2-cy1)/float(cx2-cx1)))
    if cx2<cx1 and cy2>cy1:
        tt1 = math.degrees(math.pi + math.atan((cy2-cy1)/float(cx2-cx1)))
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

    
        
    

def shift_origin(x,y):
    y = 480 - y
    return x,y


def open_by_reconstruction(src, iterations = 2, ksize = 3):
    
    # first erode the source image
    eroded = cv2.erode(src, np.ones((ksize,ksize), np.uint8), iterations=iterations)
 
     
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
    global drawing, ix, iy, jx, jy, i
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        #go = False
        #print go
        iy, ix = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(frame, (iy,ix), (x,y), (255,0,0), -1)
            
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame, (iy,ix), (x,y), (255,0,0), -1)
        jy, jx = x, y
        ux[i], uy[i], vx[i], vy[i] = ix, iy, jx, jy
        print '(', ux[i],',',  uy[i], ') {',  vx[i],',',  vy[i],')'
        i+=1
ret,frame = cap.read()

while True:
    
    
    if drawing == False:
        ret, frame = cap.read()
       
    
    cv2.setMouseCallback('frame', draw_rect)
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xFF  
    if k == 27:
        break
    
cv2.destroyAllWindows()

_, img = cap.read()
a, b = img.shape[:2]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask = np.zeros([obj_lim, a, b], np.uint8)
hist = np.zeros([obj_lim, 180, 256], np.float32)
dst = np.zeros([obj_lim, a, b], np.uint8)
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
##track_window = np.zeros([obj_lim, 4], np.uint32)
thresh = np.zeros([obj_lim, a, b], np.uint8)
    
# take first frame of the video
ret,frame = cap.read()


for n in range(0,i):
    mask[n][ux[n]:vx[n], uy[n]:vy[n]] = [255]
    
    hist[n] = cv2.calcHist([hsv], [0, 1], mask[n], [180, 256], [0, 180, 0, 256])

    cv2.normalize(hist[n],hist[n],0,255,cv2.NORM_MINMAX)

term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for n in range(0,i):
            if n!=1 and n!=2:
                dst[n] = cv2.calcBackProject([hsv],[0, 1],hist[n],[0,180, 0, 255],1)
                disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
                cv2.filter2D(dst[n],-1,disc,dst[n])
                ret,thresh[n] = cv2.threshold(dst[n],50,255,0)
                
                dst[n] = open_by_reconstruction(thresh[n])
                ret1, track_window = cv2.CamShift(abs(dst[n]), (uy[n],ux[n],abs(vy[n] - uy[n]),abs(vx[n] - ux[n])), term_crit)
                
                # Draw it on image
                pts = cv2.boxPoints(ret1)
                pts = np.int0(pts)
                cv2.polylines(frame,[pts],True, 255,2)
                dst_array = np.array(dst[0])
                noWhitePixel = 0
                cx = 0
                cy = 0
                for i0 in range(0, len(dst_array),2):
                    for j0 in range(0, len(dst_array[0]),2):
                        if dst_array[i0, j0] != 0:
                            cx += j0
                            cy += i0
                            noWhitePixel += 1

                if noWhitePixel >= 10:
                    cx /= noWhitePixel
                    cy /= noWhitePixel
                    dst[0][cy - 5:cy + 5, cx - 5:cx + 5] = 150
                xc = int((vx[0]-ux[0]+vy[0]-uy[0])/3)
                roi = frame[cy-xc:cy+xc, cx-xc:cx+xc]
                cv2.rectangle(frame, (cx-xc,cy-xc), (cx+xc, cy+xc), (255,255,0),1)
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            if i>=2:
                
                dst1 = cv2.calcBackProject([hsv_roi],[0, 1],hist[1],[0,180, 0, 255],1)
                dst2 = cv2.calcBackProject([hsv_roi],[0, 1],hist[2],[0,180, 0, 255],1)
                
                disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
                cv2.filter2D(dst1,-1,disc,dst1)
                cv2.filter2D(dst2,-1,disc,dst2)
                ret,thresh1 = cv2.threshold(dst1,50,255,0)
                ret,thresh2 = cv2.threshold(dst2,50,255,0)
                dst1 = open_by_reconstruction(thresh1, iterations = 1)
                dst2 = open_by_reconstruction(thresh2, iterations = 1)




                dst1_array = np.array(dst1)
                noWhitePixel = 0
                cx1 = 0
                cy1 = 0
                
                
                for i1 in range(0, len(dst1_array),1):
                    for j1 in range(0, len(dst1_array[0]),1):
                        if dst1_array[i1, j1] != 0:
                            cx1 += j1
                            cy1 += i1
                            noWhitePixel += 1

                if noWhitePixel >= 1:
                    cx1 /= noWhitePixel
                    cy1 /= noWhitePixel
                    dst1[cy1 - 5:cy1 + 5, cx1 - 5:cx1 + 5] = 150

                dst2_array = np.array(dst2)
                noWhitePixel = 0
                cx2 = 0
                cy2 = 0
                
                
                for i2 in range(0, len(dst2_array)):
                    for j2 in range(0, len(dst2_array[0])):
                        if dst2_array[i2, j2] != 0:
                            cx2 += j2
                            cy2 += i2
                            noWhitePixel += 1

                if noWhitePixel >= 1:
                    cx2 /= noWhitePixel
                    cy2 /= noWhitePixel
                    dst2[cy2 - 5:cy2 + 5, cx2 - 5:cx2 + 5] = 150
                cx11 = 0
                cx22 = 0
                cy11 = 0
                cy22 = 0

                cx11 = cx-xc +cx1
                cy11 = cy-xc+cy1
                cx22 = cx-xc +cx2
                cy22 = cy-xc+cy2
                dst[0][cy11 - 5:cy11 + 5, cx11 - 5:cx11 + 5] = 150
                dst[0][cy22 - 5:cy22 + 5, cx22 - 5:cx22 + 5] = 150
                
                cv2.line(frame, (cx11, cy11), (cx22,cy22), (0,255,0), 1)
                cv2.line(frame, ( 86 , 302 ) , (cx11,cy11), (0,255,0), 1)
                if cx22!=cx11:

                    cx_1, cy_1 = shift_origin(cx11, cy11)
                    cx_2, cy_2 = shift_origin(cx22, cy22)
                    cx_3, cy_3 = shift_origin(cx, cy)
                    cx_4, cy_4 = shift_origin( 86 , 302 )
                    
                    
####                    print tt
##                    print tetha

                    tt2 = calc_slope((cx_1,cy_1), (cx_2,cy_2))
                    tt1 = calc_slope((cx_1,cy_1),(cx_4,cy_4))
##                    tt2 = math.degrees(math.atan((cy22-cy11)/float(cx22-cx11)))
##                    tt1 = math.degrees(math.atan((0 - cy11)/float(0 - cx11)))

                    print 'bot line: ',tt2
                    print 'centre line : ', tt1
                    tetha = 0
##                    data = 's'
                    
                    tetha = calc_tetha(tt1,tt2)
                    print 'tetha : ', tetha
                    if abs(tetha)>15 and flag== True:
                        data = 'l'
                        print "data = ", data
                        conn = httplib.HTTPConnection(IP_addr1)
                        conn.request("HEAD", data)
                        
                        
                    else:
                        if flag == True:
                            data = 's'
                            flag = False
                        conn = httplib.HTTPConnection(IP_addr1)
                        conn.request("HEAD", data)
                        
                        if cx_3>=cx_4+10 and cx_3<=cx_4-10 and cy_3>=cy_4+10 and cy_3<=cy_4-10:
                            tt2 = calc_slope((cx_1,cy_1), (cx_2,cy_2))
                            tt1 = calc_slope((cx_1,cy_1),(cx_4,cy_4))
                            tetha = calc_tetha(tt1,tt2)
                            print 'tetha : ', tetha
                            line_track(tetha)
                        else:
                            data = 's'
                            
                        conn = httplib.HTTPConnection(IP_addr1)
                        conn.request("HEAD", data)
                        print "data = ", data   
                
                    


        a1,b1 = roi.shape[:2]
        cv2.imshow('frame',frame)
        cv2.imshow('dst',dst[0])
        
    
        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg",frame)

    else:
        break
cv2.destroyAllWindows()
cap.release()
