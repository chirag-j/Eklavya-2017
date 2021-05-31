import cv2
import numpy as np



# Create a black image, a window and bind the function to window
img = cv2.imread("Screenshot(89)", 1)


cv2.namedWindow('image', cv2.WINDOW_NORMAL)

while(1):
    cv2.imshow('image',img)
    # mouse callback function
    def print1(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            px = img[x,y]
            print px
            print("BGR value")
            a,b,c = px
            var1 = np.uint8([[[a,b,c]]])
            hsv = cv2.cvtColor(var1,cv2.COLOR_BGR2HSV)
            print("/n HSV value")
            print hsv


    
    cv2.setMouseCallback('image',print1)

    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()





