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
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
auto = auto_canny(blurred)
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
            x = abs(a2[0,0,1] - a2[2,0,1])
            y = abs(a2[2,0,0] - a2[0,0,0])
            if 13<e2<250:
                if abs(x-y)<75:
                    raw_points = a2
                    cv2.drawContours(img, c,i,(0,255,0),2 )
                    ids.append(i)
        
    i+=1
print ids
cv2.imshow('img', img)
cv2.imshow('edge', auto)
while True:
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
