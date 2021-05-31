import cv2
import numpy as np

img = cv2.imread("source.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

hist = cv2.calcHist([gray],[0],None,[256],[0,255])

#cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
back = cv2.calcBackProject([gray], [0], hist, [0,255], 1)
cv2.imshow("back", back)
cv2.imshow("gray", gray)
print hist

while True:
    k = cv2.waitKey(60) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()

#cv2.calcBackProject(images, channels, hist, ranges, scale[, dst])

