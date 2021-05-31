import numpy as np
import cv2

obj_lim = 10
ux = np.zeros([obj_lim], np.uint32)
uy = np.zeros([obj_lim], np.uint32)
i = 0
def pt(event,x,y,flags,param):
    global i
    if event == cv2.EVENT_LBUTTONDOWN:
        
        ux[i], uy[i] = x, y
        print '(', ux[i],',',  uy[i], ')'
        i+=1
img = cv2.imread('aruco.png')
while True:
    cv2.setMouseCallback('Aruco', pt)
    cv2.imshow('Aruco',img)
    if cv2.waitKey(1) ==27:
        break
cv2.destroyAllWindows()

pts1 = np.float32([[ux[0], uy[0]],[ux[1], uy[1]],[ux[2],uy[2]],[ux[3], uy[3]]])

pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,M,(300,300))
a = 0
b = 50
for i in range(0,300, 50):
    a+=50
    for j in range(0,300, 50):
        cv2.rectangle(dst, (i,j), (a,b), 255, 1)
        b+=50
    

cv2.imshow('dst',dst)
while True:
    if cv2.waitKey(1) ==27:
        break
cv2.destroyAllWindows()
