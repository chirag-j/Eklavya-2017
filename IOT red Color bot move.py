import cv2                              # Library for image processing
import numpy as np
import httplib

cap = cv2.VideoCapture(0)               # Starts video capturing on channel 1
cap.set(3, 480)

IP_addr = "192.168.43.43"               # Enter IP of WeMos D1 Mini

while True:                             # Run for infinite time
    ret, frame = cap.read()               # Capture a frame from the video stream

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,150,150])
    upper_red = np.array([30, 255, 255])

    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    
    thr_array = np.array(mask_red)

    noWhitePixel = 0
    cx = 0
    cy = 0

    for i in range(0, len(thr_array), 2):
        for j in range(0, len(thr_array[0]), 2):
            if thr_array[i, j] != 0:
                cy += i
                cx += j
                noWhitePixel += 1

    if noWhitePixel >= 1000:
        cx /= noWhitePixel
        cy /= noWhitePixel
        mask_red[cy - 5:cy + 5, cx - 5:cx + 5] = 150
        data = 's'
        if 120 < cy < 360 and 0 < cx < 140:
            data = 'l'
            print "Left"
        elif 120 < cy < 360 and 500 < cx < 640:
            data = 'r'
            print "Right"
        elif 140 < cx < 500 and 0 < cy < 120:
            data = 'f'
            print "Up"
        elif 140 < cx < 500 and 360 < cy < 480:
            data = 'b'
            print "Down"
        
        conn = httplib.HTTPConnection(IP_addr,port=None)
        conn.request("HEAD", data)

        print "No white pixels:" + str(noWhitePixel)
        print "cx: " + str(cx) + " | cy: " + str(cy)

    cv2.imshow("White Detection", mask_red)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()                           # Destroys the cap object
cv2.destroyAllWindows()                 # Destroys all the windows created by imshow
