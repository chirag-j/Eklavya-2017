import numpy as np
import glob
import cv2
def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img
mtx = np.load('mtx.npy')
dist = np.load('dist.npy')
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
images = glob.glob('*.jpg')
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((4*4,3), np.float32)
objp[:,:2] = np.mgrid[0:4,0:4].T.reshape(-1,2)
cap = cv2.VideoCapture(1)
while True:
    ret, img = cap.read()1

    
    
##    print 'corner: ', corners[0]

    if ret == True:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(gray, (4,4),None)
        if found == True:
            print "found"
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

            _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
            img = draw(img,corners2,imgpts)
        else:
            print 'not found'
        cv2.imshow('img',img)
        cv2.imshow('gray', gray)
        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()
