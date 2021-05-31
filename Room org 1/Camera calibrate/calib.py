import numpy as np
import cv2
import glob
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

images = glob.glob('*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (7,6), corners,ret)
        cv2.imshow('img',img)
        cv2.waitKey(100)

cv2.destroyAllWindows()
print 
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
print mtx
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
##for fname in glob.glob('left*.jpg'):
img = cv2.imread('left02.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
print 'corner: ', corners[0]

if ret == True:
    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

    # Find the rotation and translation vectors.
    _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
    print objp
    print corners2
    # project 3D points to image plane
    imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
    print 'pts'
    print imgpts
    img = draw(img,corners2,imgpts)
    cv2.imshow('img',img)
    while True:
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
        if k == ord('s'):
            cv2.imwrite(fname[:6]+'.png', img)

cv2.destroyAllWindows()