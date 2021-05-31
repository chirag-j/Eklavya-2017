import numpy as np
import cv2
cap = cv2.VideoCapture(0)
#img = cv2.imread("hist.jpg")
drawing = False
_, img = cap.read()
#img1 = img
a, b = img.shape[:2]

def draw_rect(event,x,y,flags,param):
    global drawing, ix, iy, jx, jy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing1 = True
        drawing = True
        iy, ix = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(img, (iy,ix), (x,y), (255,0,0), 2)
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (iy,ix), (x,y), (255,0,0), 2)
        jy, jx = x, y
        



while True:
    
    #cv2.imshow('frame', frame)
    cv2.setMouseCallback('hist', draw_rect)
    cv2.imshow('hist', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()

print ix, iy
print jx, jy
#print a,b


_, img = cap.read()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = np.zeros([a, b], np.uint8)
mask[ix:jx, iy:jy] = [255]

hist = cv2.calcHist([hsv], [0, 1], mask, [180, 256], [0, 180, 0, 256])
print hist.shape
cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
dst = cv2.calcBackProject([hsv],[0,1],hist,[0,180,0,256],1)

print 'dst shape', dst.shape

cv2.imshow("dst1", dst)
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cv2.filter2D(dst,-1,disc,dst)
ret,thresh = cv2.threshold(dst,50,255,0)
thresh = cv2.merge((thresh,thresh,thresh))
res = cv2.bitwise_and(img,thresh)
cv2.imshow("res", res)
cv2.imshow("img", img)

while True:

    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()






