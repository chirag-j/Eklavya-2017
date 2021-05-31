import numpy as np
import cv2

cap = cv2.VideoCapture(0)
drawing = False
#go = True
ret, frame = cap.read()
i = 0
obj_lim = 10
ux = np.zeros([obj_lim], np.uint32)
vx = np.zeros([obj_lim], np.uint32)
uy = np.zeros([obj_lim], np.uint32)
vy = np.zeros([obj_lim], np.uint32)
a, b = frame.shape[:2]

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
#######################################################################################################################
_, img = cap.read()
a, b = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = np.zeros([obj_lim, a, b], np.uint8)
hist = np.zeros([obj_lim, 180, 256], np.uint8)
dst = np.zeros([obj_lim, a, b], np.uint8)
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
thresh = np.zeros([obj_lim, a, b], np.uint8)
r = np.zeros([obj_lim], np.uint32)
h = np.zeros([obj_lim], np.uint32)
c = np.zeros([obj_lim], np.uint32)
w = np.zeros([obj_lim], np.uint32)

x = np.zeros([obj_lim], np.uint32)
y = np.zeros([obj_lim], np.uint32)
img = np.zeros([obj_lim, a, b, 3], np.uint8)


track_window = np.zeros([obj_lim, 4])
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )


for n in range(0,i):
    mask[n][ux[n]:vx[n], uy[n]:vy[n]] = [255]
    r[n] = ux[n]
    h[n] = vx[n] - ux[n]
    c[n] = uy[n]
    w[n] = vy[n] - uy[n]
    track_window[n] = (c[n],r[n],w[n],h[n])
    #cv2.imshow('mask0', mask[0])
    
    hist[n] = cv2.calcHist([hsv], [0, 1], mask[n], [180, 256], [0, 180, 0, 256])

    cv2.normalize(hist[n],hist[n],0,255,cv2.NORM_MINMAX)

    dst[n] = cv2.calcBackProject([hsv],[0,1],hist[n],[0,180,0,256],1)

    #cv2.imshow('dst1', dst[0])

    cv2.filter2D(dst[n],-1,disc,dst[n])

    #cv2.imshow('filterdst', dst[0])

    #thresh[n] = cv2.threshold(dst[n],50,255,0)



cv2.imshow('dst', dst[0])
while(1):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        for n in range(0,i):
            dst[n] = cv2.calcBackProject([hsv],[0, 1],hist[n],[0,180, 0, 255],1)
            cv2.filter2D(dst[n],-1,disc,dst[n])
            ret, track_window[n] = cv2.meanShift(dst[n], (c[n], r[n], w[n], h[n]), term_crit)
            c[n], r[n], w[n], h[n] = track_window[n]
            x[n],y[n],w[n],h[n] = c[n], r[n], w[n], h[n]
            img[0] = cv2.rectangle(frame, (x[0],y[0]), (x[0]+w[0],y[0]+h[0]), 255,2)
            img[n] = cv2.rectangle(img[n-1], (x[n],y[n]), (x[n]+w[n],y[n]+h[n]), 255,2)
            cv2.imshow('img',img[n])

        
        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
    else:
        break
    

cv2.destroyAllWindows()
cap.release()
