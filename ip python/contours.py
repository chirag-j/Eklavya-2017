import cv2
import numpy as np

cap = cv2.VideoCapture(1)
kernel = np.ones((4,4))
while(1):

    # Take each frame
    _, frame = cap.read()
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_red = np.array([0,100,100])
    upper_red = np.array([15, 255, 255])

    lower_green = np.array([50,50,50])
    upper_green = np.array([70, 255, 255])
    # Threshold the HSV image to get only colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    red_array = np.array(mask_red)
    noWhitePixel = 0
    cx = 0
    cy = 0
    for i in range(0, len(red_array), 2):
        for j in range(0, len(red_array[0]), 2):
            if red_array[i, j] != 0:
                cx += j
                cy += i
                noWhitePixel += 1

    if noWhitePixel >= 1000:
        cx /= noWhitePixel
        cy /= noWhitePixel
        mask_red[cy - 5:cy + 5, cx - 5:cx + 5] = 150

    print "No white pixels:" + str(noWhitePixel)
    print "cx: " + str(cx) + " | cy: " + str(cy)

    

    
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND mask and origial image
    res = cv2.bitwise_and(frame,frame, mask= mask_red)
    blur = cv2.GaussianBlur(res, (5,5), 0)
    edge = cv2.Canny(blur, 50,50)
    
    
    
    #cv2.imshow('edge',edge)
    cv2.imshow('frame',frame)
    cv2.imshow('mask red',mask_red)
    #cv2.imshow('mask green',mask_green)
    #cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
