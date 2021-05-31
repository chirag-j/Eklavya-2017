import cv2
import numpy as np
i = 0
def open_by_reconstruction(src, iterations = 1, ksize = 3):
    global i
    # first erode the source image
    eroded = cv2.erode(src, np.ones((ksize,ksize), np.uint8), iterations=iterations)
 
    # Now we are going to iteratively regrow the eroded mask.
    # The key difference between just a simple opening is that we
    # mask the regrown everytime with the original src.
    # Thus, the dilated mask never extends beyond where it does in the original.
    
    this_iteration = eroded
    last_iteration = eroded
    while (True):
        this_iteration = cv2.dilate(last_iteration, np.ones((ksize,ksize), np.uint8), iterations = 1)
        this_iteration = this_iteration & src
        i+=1
        if np.array_equal(last_iteration, this_iteration):
            # convergence!
            break
        last_iteration = this_iteration.copy()
       
    return this_iteration




img = cv2.imread('full.jpg')
checker = cv2.imread('hist.jpg')
patt = cv2.imread('patt.jpg')
hsvi= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv = cv2.cvtColor(patt, cv2.COLOR_BGR2HSV)
hist = cv2.calcHist([hsv], [0, 1], None , [180, 256], [0, 180, 0, 256])

dst = cv2.calcBackProject([hsvi],[0,1],hist,[0,180,0,256],1)
cv2.imshow('dst', dst)
ret, dst = cv2.threshold(dst,50, 255, cv2.THRESH_BINARY)
dst = open_by_reconstruction(dst)
print i
cv2.imshow('img', img)
cv2.imshow('dst1', dst)

while True:
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
