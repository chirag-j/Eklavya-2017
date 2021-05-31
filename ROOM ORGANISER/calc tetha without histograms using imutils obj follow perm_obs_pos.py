import cv2
import numpy as np
import math
import time
from imutils.video import WebcamVideoStream
import httplib
IP_addr1 = "192.168.43.53"
data = 's'
fi = 0
ipl = 0
co = 0
ipl = 0
x = np.zeros([100], np.uint8)
y = np.zeros([100], np.uint8)
drawing = False
perm_obs_pos = False
ux = []
uy = []
vx = []
vy = []
px1 = []
py1 = []
px2 = []
py2 = []
ipop = 0
cap = WebcamVideoStream(src = 0).start()
ir = 0
abx = 0
aby = 0
def line_track(tetha):
    global data
    if abs(tetha)>5:
        if tetha>5:
            data = 'r'
       

        if tetha<-5:
            data = 'l'
        
    else :
        data = 'f'
    
    return data
def bot_align(tetha):
    if abs(tetha)>5:
        
        if tetha>5:
            data = 'r'
       

        if tetha<-5:
            data = 'l'
        
    else :
        data = 's'
    
    return data

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
def fill(a):
    global fi, ab
    fi+=1
    ab =0
    for bf in range(0,len(a)):
        for cf in range(0,len(a[0])):
            if a[bf,cf] == fi-1:
                x[ab],y[ab] = bf, cf
                ab+=1
            
                
    for n in range(0,ab):
        
        if x[n]>0 and y[n]>0 and x[n]<(len(a)-1) and y[n]<(len(a[0])-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = fi
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = fi
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = fi
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = fi
                
           
            
        elif x[n]>0 and y[n]==0 and x[n]<(len(a)-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = fi
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = fi
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = fi
                
            
                

        elif x[n]==0 and y[n]>0 and y[n]<(len(a[0])-1):
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = fi
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = fi
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = fi

            
            
                    
        elif y[n]>0 and x[n]==(len(a)-1) and y[n]<(len(a[0])-1):
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = fi
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = fi
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = fi          
            
            
                
        elif x[n]>0 and x[n]<(len(a)-1) and y[n]==(len(a[0])-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = fi
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = fi
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = fi

           

        elif x[n]==0 and y[n]==0:
            if(a[x[n]+1,y[n]] == 100):
                a[x[n]+1, y[n]] = fi
            if(a[x[n],y[n]+1] == 100):
                a[x[n],y[n]+1] = fi
            
           

        elif x[n]==(len(a)-1) and y[n]==(len(a[0])-1):
            if (a[x[n]-1,y[n]]==100):
                a[x[n]-1,y[n]] = fi
            if(a[x[n],y[n]-1] == 100):
                a[x[n],y[n]-1] = fi

      
    for fb in range(0,len(a)):
        for fc in range(0,len(a[0])):
            if a[fb,fc] == 100 and fi<50:
                fill(a)
    if fi>50:
        print fi


def plan_path(a, x, y):
    global ptp, ipl
    ptp = np.zeros([a[x,y]+1, 2], np.uint8)
    ptp[0] = y, x
    while a[x,y]!=0:
        ipl+=1
        if x>0 and y>0 and x<(len(a)-1) and y<(len(a[0])-1):
            if (a[x-1,y]<a[x,y]):
                ptp[ipl] = y, x-1
                x, y = x-1, y
            elif(a[x+1,y] <a[x,y]):
                ptp[ipl] = y,x+1
                x, y = x+1, y
            elif(a[x,y-1] <a[x,y]):
                ptp[ipl] = y-1, x
                x, y = x, y-1
            elif(a[x,y+1] <a[x,y]):
                ptp[ipl] = y+1, x
                x, y = x, y+1
                
           
            
        elif x>0 and y==0 and x<(len(a)-1):
            if (a[x-1,y]<a[x,y]):
                ptp[ipl] = y, x-1
                x, y = x-1, y
            elif(a[x+1,y] <a[x,y]):
                ptp[ipl] = y,x+1
                x, y = x+1, y
            elif(a[x,y+1] <a[x,y]):
                ptp[ipl] = y+1,x
                x, y = x, y+1
                
            
                

        elif x==0 and y>0 and y<(len(a[0])-1):
            if(a[x,y-1] <a[x,y]):
                ptp[ipl] = y-1,x
                x, y = x, y-1
            elif(a[x,y+1] <a[x,y]):
                ptp[ipl] = y+1,x
                x, y = x, y+1
            elif(a[x+1,y] <a[x,y]):
                ptp[ipl] = y,x+1
                x, y = x+1, y

            
            
                    
        elif y>0 and x==(len(a)-1) and y<(len(a[0])-1):
            if(a[x,y-1] <a[x,y]):
                ptp[ipl] = y-1,x
                x, y = x, y-1
            elif(a[x,y+1] <a[x,y]):
                ptp[ipl] = y+1,x
                x, y = x, y+1
            elif (a[x-1,y]<a[x,y]):
                ptp[ipl] = y,x-1
                x, y = x-1, y
            
            
                
        elif x>0 and x<(len(a)-1) and y==(len(a[0])-1):
            if (a[x-1,y]<a[x,y]):
                ptp[ipl] = y,x-1
                x, y = x-1, y
            elif(a[x+1,y] <a[x,y]):
                ptp[ipl] = y,x+1
                x, y = x+1, y
            if(a[x,y-1] <a[x,y]):
                ptp[ipl] = y-1,x
                x, y = x, y-1

           

        elif x==0 and y==0:
            if(a[x+1,y] <a[x,y]):
                ptp[ipl] = y,x+1
                x, y = x+1, y
            elif(a[x,y+1] <a[x,y]):
                ptp[ipl] = y+1,x
                x, y = x, y+1
            
           

        elif x==(len(a)-1) and y==(len(a[0])-1):
            if (a[x-1,y]<a[x,y]):
                ptp[ipl] = y,x-1
                x, y = x-1, y
            elif(a[x,y-1] <a[x,y]):
                ptp[ipl] = y-1,x
                x, y = x, y-1

    return ptp

    
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
    global drawing, ix, iy, jx, jy, ir, abx, aby, frame_hsv, perm_obs_pos, ipop
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
        if perm_obs_pos == False:
            if abs(jx-ix)>10 and abs(jy-iy)>10:
                ux.append(ix)
                uy.append(iy)
                vx.append(jx)
                vy.append(jy)
                print "Object Stored. Object ID : ",ir
                ir+=1
            else:
                print "Object was too small"
        else:
            if abs(jx-ix)>10 and abs(jy-iy)>10:
                px1.append(ix)
                py1.append(iy)
                px2.append(jx)
                py2.append(jy)
                print "Obstacle Stored. Obstacle ID : ",ipop
                ipop+=1
            else:
                print "Obstacle was too small."
            

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
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        if ir>=3:
            break
        else:
            print "Please Select Atleast Three Rectangles"
            print "1st Rect : Bot Head"
            print "2st Rect : Bot Tail"
            print "3st Rect : First Object"
    elif k == ord('o'):
        if perm_obs_pos == False:
            perm_obs_pos = True
            print "Obstacle Mode On"
        else:
            perm_obs_pos = False
            print "Obstacle Mode Off"

       
cv2.destroyAllWindows()
print "Total Objects : ", ir
print "Total Obstacles : ", ipop

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
frame = cap.read()
frame_h = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
brx = np.zeros([ir], np.uint32)
bry = np.zeros([ir], np.uint32)
brw = np.zeros([ir], np.uint32)
brh = np.zeros([ir], np.uint32)
max_area = []
for ls in range(0,ir):
    mask[ls] = cv2.inRange(frame_h, lower_range[ls], upper_range[ls])
    mask[ls] = open_by_reconstruction(mask[ls])
    i, c, h = cv2.findContours(mask[ls], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(c)>0:
        max_area1 = 0
        counter = 0
        for n in c:
            a = cv2.contourArea(n)
            if a>max_area1:
                max_area1 = a
                idc = counter
            counter+=1
        max_area.append(max_area1)
        brx[ls], bry[ls], brw[ls], brh[ls] = cv2.boundingRect(c[idc])
##        cv2.rectangle(frame, (brx[ls], bry[ls]), (brx[ls] + brw[ls], bry[ls] + brh[ls]), (0,255,0), 2)
        M = cv2.moments(c[idc])
        cx[ls] = int(M['m10']/M['m00'])
        cy[ls] = int(M['m01']/M['m00'])
    else:
        print "Obj id no", ir, "not found"

wb = int(math.sqrt(max_area[0]+max_area[1]))
arx = int(640/wb +1)
ary = int(480/wb +1)
print ary, arx
map_array = np.full([ary,arx], 100, np.uint8)
mask_map = np.zeros([480,640,3], np.uint8)

for xg in range(2,ir):
    mask_map[int(bry[xg]) : int((bry[xg]+brh[xg])+1), int(brx[xg]) : int((brx[xg]+brw[xg])+1)] = (255,255,255)
    map_array[int(bry[xg]/wb) : int(((bry[xg]+brh[xg])/wb)+1), int(brx[xg]/wb) : int(((brx[xg]+brw[xg])/wb)+1)] = 255
for xg in range(0,ipop):
    mask_map[int(py1[xg]) : int((py2[xg])+1), int(px1[xg]) : int((px2[xg])+1)] = (255,255,255)
    map_array[int(py1[xg]/wb) : int(((py2[xg])/wb)+1), int(px1[xg]/wb) : int(((px2[xg])/wb)+1)] = 255
ag = 0
bg = wb
for xg in range(0, 640, wb):
    ag=xg+wb
    for yg in range(0, 480, wb):
        cv2.rectangle(mask_map, (xg,yg), (ag,bg), (0,255,255), 1)
        bg+=wb
map_array[int(cy[0]/wb), int(cx[0]/wb)] = 0
print map_array
fill(map_array)
print map_array

cv2.imshow('mask_map', mask_map)
clamp_close = False
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
##            brx[ls], bry[ls], brw[ls], brh[ls] = cv2.boundingRect(c[idc])
##            cv2.rectangle(frame, (brx[ls], bry[ls]), (brx[ls] + brw[ls], bry[ls] + brh[ls]), (0,255,0), 2)
            wc = math.sqrt(max_area)
            wc = int(1.5 * wc)
            M = cv2.moments(c[idc])
            cx[ls] = int(M['m10']/M['m00'])
            cy[ls] = int(M['m01']/M['m00'])
##            roi2 = frame[abs(int(cy-(wc/2))):cy+(wc/2), abs(int(cx-(wc/2))):cx+(wc/2)]
            mask[ls][cy[ls]-5:cy[ls]+5, cx[ls]-5:cx[ls]+5] = 155
            cv2.drawContours(frame, c, idc, (255, 0, 0), 2)
        else:
            print "obj no", ir, "not found"
            
    cv2.line(frame, (cx[0], cy[0]), (cx[1],cy[1]), (0,255,0), 1)
    cv2.line(frame, ( abx, aby) , (cx[1],cy[1]), (0,255,0), 1)
    cx0, cy0 = shift_origin(cx[0], cy[0])
    cx1, cy1 = shift_origin(cx[1], cy[1])
    abxs, abys = shift_origin(cx[2], cy[2])
    cx0, cy0, cx1, cy1, abxs, abys = int(cx0), int(cy0), int(cx1), int(cy1), int(abxs), int(abys)
    if cx1!=cx0 and cx1!=abxs:
##        print "cx1, cy1: ", cx1, cy1
##        print "cx0, cy0: ", cx0, cy0
##        print "cy0 - cx1 : ", float(cy0 - cy1)
##        print "cx0 - cx1: ", float(cx0 - cx1)
        slope_bot = calc_slope((cx1, cy1),(cx0, cy0))
        slope_t = calc_slope((cx1, cy1),(abxs, abys))
##        print "slope bot :", slope_bot
##        print "slope target :", slope_t
        tetha = calc_tetha(slope_bot, slope_t)
        abx, aby = cx[2], cy[2]
##        print "tetha : ",tetha
        if clamp_close is False:
            if cx[0]<abx-80 or cx[0]>abx+80 or cy[0]<aby-80 or cy[0]>aby+80:
                cv2.rectangle(frame, (abx+80, aby+60), (abx-80, aby-80), (255,255,0), 2)
                data = line_track(tetha)
            else:
                if abs(tetha)>5:
                    data = bot_align(tetha)
                else:
                    data = 'c'
                    clamp_close = True
        else:
            data = 's'
                    

        if data!=None:
            pass
##            conn = httplib.HTTPConnection(IP_addr1)
##            conn.request("HEAD", data)
##            print "data = ", data
        else:
            print 'data is none'


    
    mask_bot = mask[0] + mask[1]
##    cv2.imshow('img', frame)
##    cv2.imshow('mask', mask_bot)
##    print time.time()
    if cv2.waitKey(1)  == 27:
        break

cv2.destroyAllWindows()
data = 's'
##conn = httplib.HTTPConnection(IP_addr1)
##conn.request("HEAD", data)
