import cv2
import numpy as np

cap = cv2.VideoCapture(0)
kernel = np.ones((4,4))

def open_by_reconstruction(src, iterations = 3, ksize = 3):
    
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
        
        if np.array_equal(last_iteration, this_iteration):
            # convergence!
            break
        last_iteration = this_iteration.copy()
       
    return this_iteration
while(1):

    # Take each frame
    _, frame = cap.read()
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_red = np.array([0,100,50])
    upper_red = np.array([20, 255, 255])

    lower_green = np.array([110,50,50])
    upper_green = np.array([130, 255, 255])
    # Threshold the HSV image to get only colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_red = open_by_reconstruction(mask_red)
    edge = cv2.Canny(mask_red, 50,50)
    cv2.imshow('edge', edge)

    image, contours, hierarchy = cv2.findContours(edge,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #print contours
    img = cv2.drawContours(frame, contours, -1, (0,255,0), 3)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    # Bitwise-AND mask and original image
  #  res = cv2.bitwise_and(frame,frame, mask= mask_red)
 #   blur = cv2.GaussianBlur(res, (5,5), 0)
#    edge = cv2.Canny(blur, 50,50)
    
    
    
    #cv2.imshow('edge',edge)
    cv2.imshow('frame',frame)
    cv2.imshow('mask red',mask_red)
    #cv2.imshow('mask green',mask_green)
    #cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
