import cv2
import numpy as np
import math
import httplib
cap = cv2.VideoCapture(0)               # Starts video capturing on channel 1
IP_addr = "192.168.43.133"
#data = "f"
# Take each frame
tetha1 = 0
tetha2 = 0
while True:
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([100,50,50])
    upper_blue = np.array([120,255,255])
    lower_red = np.array([0,150,100])
    upper_red = np.array([30,255,255])
    lower_green = np.array([50,100,100])
    upper_green = np.array([70,255,255])

    # Threshold the HSV image to get only blue colors
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    mask = blue_mask + red_mask + green_mask
    res = cv2.bitwise_and(frame,frame,mask= mask)
    ret,thresh = cv2.threshold(mask,127,255,0)
    
    # Bitwise-AND mask and original image
    
    mask_array = np.array(blue_mask)
    noWhitePixel = 0
    cx1 = 0
    cy1 = 0
    for i in range(0, len(mask_array), 2):
        for j in range(0, len(mask_array[0]), 2):
            if mask_array[i, j] != 0:
                cx1 += j
                cy1 += i
                noWhitePixel += 1

    if noWhitePixel >= 1000:
        cx1 /= noWhitePixel
        cy1 /= noWhitePixel
        mask[cy1 - 5:cy1 + 5, cx1 - 5:cx1 + 5] = 150
   # Convert BGR to HSV
    # define range of blue color in HSV
    
    

    
    mask_array = np.array(red_mask)
    noWhitePixel = 0
    cx2 = 0
    cy2 = 0
    for i in range(0, len(mask_array), 2):
        for j in range(0, len(mask_array[0]), 2):
            if mask_array[i, j] != 0:
                cx2 += j
                cy2 += i
                noWhitePixel += 1

    if noWhitePixel >= 1000:
        cx2 /= noWhitePixel
        cy2 /= noWhitePixel
        mask[cy2 - 5:cy2 + 5, cx2 - 5:cx2 + 5] = 0


    mask_array = np.array(green_mask)
    noWhitePixel = 0
    cx3 = 0
    cy3 = 0
    for i in range(0, len(mask_array), 2):
        for j in range(0, len(mask_array[0]), 2):
            if mask_array[i, j] != 0:
                cx3 += j
                cy3 += i
                noWhitePixel += 1

    if noWhitePixel >= 1000:
        cx3 /= noWhitePixel
        cy3 /= noWhitePixel
        mask[cy3 - 5:cy3 + 5, cx3 - 5:cx3 + 5] = 255     


    print "No white pixels:" + str(noWhitePixel)
    print "cx1: " + str(cx1) + " | cy1: " + str(cy1) + "| cx2: " + str(cx2) + " | cy2: " + str(cy2) + "|cx3: " + str(cx3) + " |cy3: " + str(cx1)  
    print "No white pixels:" + str(noWhitePixel)
    cv2.imshow("red & blue detect",mask)
    cv2.imshow("frame",frame)
    if cx1!=cx2:
        tetha1 = math.degrees(math.atan((cy2-cy1)/float(cx2-cx1)))
        print 'Tetha1', tetha1
    if tetha1>0:
       data="r"
    elif tetha1<0:
        data = "l"
    else:
       data="s"
       
    print 'data = ' + data
    conn = httplib.HTTPConnection(IP_addr)
    conn.request("HEAD", data)
       
    cv2.imshow("frame",frame)
    cv2.imshow("red and blue",mask)
    #cv2.imshow("red mask",red_mask)
    #v2.imshow("blue mask",blue__mask)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()                           # Destroys the cap object
cv2.destroyAllWindows()                 # Destroys all the windows created by imshow


