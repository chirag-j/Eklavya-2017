import numpy as np
import cv2
import math
import httplib
IP_addr1 = "192.168.43.53"
cap = cv2.VideoCapture(0)
flag = True
flag1 = True
flag2 = False
drawing = False
#go = True
ret, frame = cap.read()
i = 0
obj_lim = 10
ux = np.zeros([obj_lim], np.uint32)
vx = np.zeros([obj_lim], np.uint32)
uy = np.zeros([obj_lim], np.uint32)
vy = np.zeros([obj_lim], np.uint32)
x = np.zeros([100], np.uint8)
y = np.zeros([100], np.uint8)
fi = 0
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
ipl = 0
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
            elif(a[x,y-1] <a[x,y]):
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
def line_track(tetha):
    global data
    
##    print 'hi'
    if abs(tetha)>5:
        
        if tetha>5 and tetha<15:
            data = 'l'
        elif tetha>15 and tetha<20:
            data = 'l'
        elif tetha>20 and tetha<30:
            data = 'l'
        elif tetha>30:
            data = 'l'

        if tetha<-10 and tetha>-15:
            data = 'r'
        elif tetha<-15 and tetha>-20:
            data = 'r'
        elif tetha<-20 and tetha>-30:
            data = 'r'
        elif tetha<-30:
            data = 'r'
    else :
        data = 'f'
    
    return data
        
    
        
            
    
    

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
    global drawing, ix, iy, jx, jy, i, abx, aby
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        #go = False
        #print go
        ix,iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(frame, (ix,iy), (x,y), (255,0,0), -1)
            
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame, (ix, iy), (x,y), (255,0,0), -1)
        jx, jy = x, y
        ux[i], uy[i], vx[i], vy[i] = ix, iy, jx, jy
        print '(', ux[i],',',  uy[i], ') {',  vx[i],',',  vy[i],')'
        i+=1

    elif event == cv2.EVENT_RBUTTONDOWN:
        abx, aby = x, y
        print 'abx : ', abx, '  aby: ', aby
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
maskx = np.zeros([a, b, 3], np.uint8)

hist = np.zeros([obj_lim, 180, 256], np.float32)
dst = np.zeros([obj_lim, a, b], np.uint8)
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
thresh = np.zeros([obj_lim, a, b], np.uint8)





for n in range(3,i):
    mask[n][ux[n]:vx[n], uy[n]:vy[n]] = [255]
    maskx[ux[n]:vx[n], uy[n]:vy[n]] = [255]

    hist[n] = cv2.calcHist([hsv], [0, 1], mask[n], [180, 256], [0, 180, 0, 256])

    cv2.normalize(hist[n],hist[n],0,255,cv2.NORM_MINMAX)

#############path plan######
w = int((vx[0]-ux[0]+vy[0]-uy[0])/2)
ag = 0
bg = w
for xg in range(0, 640, w):
    ag=xg+w
    for yg in range(0, 480, w):
        cv2.rectangle(maskx, (xg,yg), (ag,bg), (0,255,255), 1)
        bg+=w
cv2.imshow('maskx', maskx)
dsti = cv2.calcBackProject([hsv],[0, 1],hist[i-1],[0,180, 0, 255],1)
dst_arrayi = np.array(dsti)
noWhitePixel = 0
cxi = 0
cyi = 0
print a/w, b/w
print a, b
print w
arr = np.full([(a/w)+1, (b/w)+1], 100, np.uint8)

for i0 in range(0, len(dst_arrayi),2):
    for j0 in range(0, len(dst_arrayi[0]),2):
        if dst_arrayi[i0, j0] != 0:
            cxi += j0
            cyi += i0
            noWhitePixel += 1

if noWhitePixel >= 10:
    cxi /= noWhitePixel
    cyi /= noWhitePixel

arr[cyi/w, cxi/w] = 0
for xg in range(0,i-1):
    arr[uy[xg]/w : vy[xg]/w+1, ux[xg]/w : vx[xg]/w+1] = 255

print arr
############path plan ends##############
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
                
                dst[n] = open_by_reconstruction(thresh[n], iterations = 3)
##                ret1, track_window = cv2.CamShift(abs(dst[n]), (uy[n],ux[n],abs(vy[n] - uy[n]),abs(vx[n] - ux[n])), term_crit)
                
                # Draw it on image
##                pts = cv2.boxPoints(ret1)
##                pts = np.int0(pts)
##                cv2.polylines(frame,[pts],True, 255,2)
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
    

                cx11 = cx-xc +cx1
                cy11 = cy-xc+cy1
                cx22 = cx-xc +cx2
                cy22 = cy-xc+cy2
                dst[0][cy11 - 5:cy11 + 5, cx11 - 5:cx11 + 5] = 150
                dst[0][cy22 - 5:cy22 + 5, cx22 - 5:cx22 + 5] = 150
                
##                cv2.line(frame, (cx11, cy11), (cx22,cy22), (0,255,0), 1)
##                cv2.line(frame, ( abx, aby) , (cx11,cy11), (0,255,0), 1)
##                if cx22!=cx11 and cx11!=abx:
##
##                    cx_1, cy_1 = shift_origin(cx11, cy11)
##                    cx_2, cy_2 = shift_origin(cx22, cy22)
##                    cx_3, cy_3 = shift_origin(cx, cy)
##                    cx_4, cy_4 = shift_origin( abx, aby )
##                    
##                    
##                    tt2 = calc_slope((cx_1,cy_1), (cx_2,cy_2))
##                    tt1 = calc_slope((cx_1,cy_1),(cx_4,cy_4))
##
##                    print 'bot line: ',tt2
##                    print 'centre line : ', tt1
##                    tetha = 0
##                    
##                    tetha = calc_tetha(tt1,tt2)
##                    print 'tetha : ', tetha
##                        
##                        
##                    
##                    
##                    if cx<abx-20 or cx>abx+20 or cy<aby-20 or cy>aby+2:
##                        cv2.rectangle(frame, (abx+20, aby+20), (abx-20, aby-20), (255,255,0), 2)
##                        data = line_track(tetha)
##                    if data!=None:
####                        conn = httplib.HTTPConnection(IP_addr1)
####                        conn.request("HEAD", data)
##                        print "data = ", data
##                    else:
##                        print 'data is none'
        cv2.imshow('frame',frame)
        cv2.imshow('dst',dst[0])
        
    
        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break

    else:
        print 'ret is false'
        break
cv2.destroyAllWindows()
cap.release()
data = 's'
##conn = httplib.HTTPConnection(IP_addr1)
##conn.request("HEAD", data)
