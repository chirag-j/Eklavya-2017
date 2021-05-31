import numpy as np
import cv2

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
 
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
 
    # return the edged image
    return edged
img = cv2.imread("aruco.png")
cont = cv2.imread("aruco.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
##auto = auto_canny(blurred)
auto = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,31,10)

i, c, h = cv2.findContours(auto,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
i = 0
ids = []

for x in c:
    k = cv2.isContourConvex(x)
    if k == True:
        pass
    else:
        e2 = 0.1*cv2.arcLength(x,True)
        
        a2 = cv2.approxPolyDP(x, e2, True)
        if len(a2) == 4:
            cy = abs(a2[0,0,1] - a2[2,0,1])
            cx = abs(a2[2,0,0] - a2[0,0,0])
            if 10<e2<250:
                if 15<abs(cx-cy)<50:
                    print a2
                    cv2.drawContours(cont, c,i,(0,255,0),1 )
                    ids.append(i)
    i+=1
cnt = c[ids[0]]

##x,y,w,h = cv2.boundingRect(c[])
e2 = 0.1*cv2.arcLength(cnt,True)
a2 = cv2.approxPolyDP(cnt, e2, True)
pt = a2.ravel().reshape(4,2)
print a2
print pt
pts1 = np.float32([pt[0], pt[1], pt[2], pt[3]])
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

##pts1 = cv2.cornerSubPix(gray,pts1,(11,11),(-1,-1),criteria)
pts2 = np.float32([[0,0],[0,300],[300,300],[300,0]])
##pts2 = np.float32([[0,0],[300,0],[300,300],[0,300]])

M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,M,(300,300))
gray_dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
ret2,gray_dst = cv2.threshold(gray_dst,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
print 'ret2: ', ret2
i1, c1, h1 = cv2.findContours(gray_dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
ct = 0
ar = []
for ls in c1:
    a = cv2.contourArea(ls)
    ar.append(a)
blob = ar.index(max(ar))
cv2.drawContours(dst, c1,blob,(0,255,0),1 )


x,y,w,h = cv2.boundingRect(c1[blob])
cv2.rectangle(gray_dst,(x,y),(x+w,y+h),(0,255,0),2)
##gray_dst = gray_dst[y:y+h, x:x+w]
a = 0
b = 300/8
b1 = b
a1 = 300/8
array = np.zeros([8, 8], np.uint8)
c1 = 0
c2 = 0
for i in range(0,300-a1,a1):

    a+=a1
    c2 = 0
    for j in range(0,300-b1, b1):
        
        cv2.rectangle(gray_dst, (i,j), (a,b), 255, 1)
        cx = int(i + (300/16))
        cy = int(j + (300/16))
        if gray_dst[cy, cx] == 255:
            array[c2,c1] = 1
        b+=b1
        c2+=1
    c1+=1
print ids
print c1, c2
print array
cv2.imshow('gray_dst', gray_dst)

##cv2.imshow('dst', dst)
cv2.imshow('cnt', cont)
cv2.imshow('gray', gray)
cv2.imshow('auto', auto)
##cv2.imshow('img', img)
##cv2.imshow('edge', auto)
while True:
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
