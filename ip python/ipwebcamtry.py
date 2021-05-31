import cv2
import numpy as np
import urllib
import math


url = 'http://192.168.0.100:8080/shot.jpg?rnd=982507'

while True:
    imgResp = urllib.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    
    cv2.imshow("img", img)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
