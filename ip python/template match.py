import cv2
import numpy as np

source = cv2.imread('Capture1.jpg')
temp = cv2.imread('hist.jpg')
##source.astype(np.float32)
##temp.astype(np.float32)
s_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
t_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

w, h = temp.shape[:2]

res = cv2.matchTemplate(s_gray, t_gray, cv2.TM_CCOEFF_NORMED)
threshold = 0.8

##print res

max_arr = np.zeros([len(res)])
for n in range(0, len(res)):
    
    max_arr[n] = max((res[n]))
    
thresh = max(max_arr)


print thresh
loc = np.where(res==thresh)
print loc

pt = zip(*loc)[0]
print pt
y,x = pt

cv2.circle(source, (x+h/2,y+h/2), h/2, (0,255,255), 1)
cv2.imshow('detected', source)
while True:
    k = cv2.waitKey(60) & 0xff
    if k == 27:
        break
    
        

cv2.destroyAllWindows()

        
