import numpy as np
import cv2
import glob
import time
def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    print corner
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

cap = cv2.VideoCapture(1)
i = 0
while i<14:
    ret, img = cap.read()
    if ret == True:
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow('img',img)
        

        # Find the chess board corners
        found, corners = cv2.findChessboardCorners(gray, (7,6),None)

        # If found, add object points, image points (after refining them)
        if found == True:
            print 'Found!!!!!!!!!!!!!!'
            i+=1
            print 'i: ', i
            objpoints.append(objp)
            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners)
            cv2.imwrite("C:\Users\Chirag\Documents\Bluetooth Folder\Calibration"+chr(i+96)+"1.jpg", gray)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, (7,6), corners, ret)
##            cv2.imwrite(chr(i+96)+".jpg", img)
            cv2.imshow('img',img)
            time.sleep(3)
##            cv2.waitKey(5000)
        else:
            print "not found"
        if cv2.waitKey(1) == 27:
            break
##            
    else:
        print 'ret: ', ret
        break
cv2.destroyAllWindows()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
print mtx
np.save('mtx.npy', mtx)
np.save('dist.npy', dist)



