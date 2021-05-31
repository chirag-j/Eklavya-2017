import cv2
import numpy as np
cap = np.zeros([400,400], np.uint8)
cv2.imshow("w", cap)
while True:
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

#print frame.shape
