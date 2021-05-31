import cv2
import numpy as np
import urllib

#cap = cv2.VideoCapture(3)
kernel = np.ones((4,4))
url = 'http://192.168.0.100:8080/shot.jpg?rnd=982507'
while(1):

    # Take each frame
##    _, frame = cap.read()
    imgResp = urllib.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgNp, -1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,50, 255,0)
    mask = cv2.bitwise_not(thresh)
    cv2.imshow('mask', mask)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_red = np.array([0,150,50])
    upper_red = np.array([20, 255, 255])

    lower_green = np.array([0,55,55])
    upper_green = np.array([0, 255, 255])
    # Threshold the HSV image to get only colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

   # edge = cv2.Canny(mask_red, 1000, 1000)
  #  image, contours, hierarchy = cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
 #   img = cv2.drawContours(frame, contours, -1, (0,255,0), 3)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
   # mask_two = cv2.add(mask_red, mask_green)

  #  # Bitwise-AND mask and origial image
 #   res = cv2.bitwise_and(frame,frame, mask= mask_red)
#    blur = cv2.GaussianBlur(res, (5,5), 0)
    
    
    
    
    #cv2.imshow('mask2',mask_two)
    cv2.imshow('frame',frame)
    cv2.imshow('mask red',mask_red)
    cv2.imshow('mask green',mask_green)
    #cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
