import cv2
import numpy as np
img = cv2.imread('aruco.png')
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
##cv2.imshow('aruco', img_g)
th2 = cv2.adaptiveThreshold(img_g,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,27,9)
i, c, h = cv2.findContours(th2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##th2 =  th2 & th2 & th2
cv2.imshow('thresh', th2)
i = 0
for x in c:
    k = cv2.isContourConvex(x)
    if k == True:
        cv2.drawContours(img, c,i,(0,255,0),2 )
    elif k == False:
        pass
    i+=1
##cv2.drawContours(img, c,-1,(0,255,0),2 )
##cv2.imshow('cnt',th2)
cv2.imshow('img', img)
while(1):
    if cv2.waitKey(10) == 27:
        break
cv2.destroyAllWindows()
