import numpy as np
import cv2

# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
img = cv2.line(img,(0,0),(511,511),(255,0,0),5)
while True:
    cv2.imshow('line',img)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
