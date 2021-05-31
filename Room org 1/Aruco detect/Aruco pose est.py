import numpy as np
import cv2
def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img
def ismarkerpresent(img):
    i, c, h = cv2.findContours(auto,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    ids = []
    for x in c:
        k = cv2.isContourConvex(x)
        if k == False:
            e2 = 0.1*cv2.arcLength(x,True)
            a2 = cv2.approxPolyDP(x, e2, True)
            if len(a2) == 4:
                cy = abs(a2[0,0,1] - a2[2,0,1])
                cx = abs(a2[2,0,0] - a2[0,0,0])
                if 30<e2<250:
                    if 30<abs(cx-cy)<50:
                        
                        cv2.drawContours(img, c,i,(0,255,0),2 )
                        ids.append(i)
        i+=1
def marker_id(mat):
    line1 = mat[1:6, 2]
    line2 = mat[1:6, 4]
    i = 4
    s = 0
    for n in range(1,10,2):
        sum1 = s + line1[i]*(2**n)
        s = sum1
        i-=1
    i=4
    for n in range(0,9,2):
        sum1 = s + line2[i]*(2**n)
        s = sum1
        i-=1

    print (line1)
    print (line2)
    return s
    

    
def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged
##img = cv2.imread("aruco.png")
##cont = cv2.imread("aruco.png")



cap = cv2.VideoCapture(1)
axis = np.float32([[1,0,0], [0,1,0], [0,0,-1]]).reshape(-1,3)
mtx = np.load('mtx.npy')
dist = np.load('dist.npy')
objp = np.zeros((2*2,3), np.float32)
objp[:,:2] = np.mgrid[0:2,0:2].T.reshape(-1,2)
while True:
    ret, img = cap.read()
    if ret is True:
        org = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    ##    auto = auto_canny(blurred)
        auto = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,10)
        i, c, h = cv2.findContours(auto,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        ids = []
        detected = False
        for x in c:
            k = cv2.isContourConvex(x)
            if k == False:
                e2 = 0.1*cv2.arcLength(x,True)
                a2 = cv2.approxPolyDP(x, e2, True)
                if len(a2) == 4:
                    cy = abs(a2[0,0,1] - a2[2,0,1])
                    cx = abs(a2[2,0,0] - a2[0,0,0])
    ##                if 20<e2<100:
    ##                    if 30<abs(cx-cy)<100:
                    if 10000<cv2.contourArea(x)<30000:
                        print (cx-cy)
                        print (e2)
                        print ('area: ', cv2.contourArea(x))
                        ids.append(i)
                        detected = True
            i+=1
        if detected:
            cv2.drawContours(img, c,ids[0],(0,255,0),2 )
            cnt = c[ids[0]]

            ##x,y,w,h = cv2.boundingRect(c[])
            e2 = 0.1*cv2.arcLength(cnt,True)
            a2 = cv2.approxPolyDP(cnt, e2, True)
            pt = a2.ravel().reshape(4,2)
            print (a2)
            print (pt)
            pts1 = np.float32([pt[0], pt[1], pt[2], pt[3]])
            if np.cross(pt[0],pt[1])<0:
                pts1 = np.float32([pt[0], pt[3], pt[2], pt[1]])
            s = marker_id(array)
                
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

            ##pts1 = cv2.cornerSubPix(gray,pts1,(11,11),(-1,-1),criteria)
            ##pts2 = np.float32([[0,0],[0,300],[300,300],[300,0]])
            pts2 = np.float32([[0,0],[300,0],[300,300],[0,300]])

            M = cv2.getPerspectiveTransform(pts1,pts2)
            dst = cv2.warpPerspective(org,M,(300,300))
            gray_dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
            ret2,gray_dst = cv2.threshold(gray_dst,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            print ('ret2: ', ret2)
            a = 0
            b = 300/7
            b1 = b
            a1 = 300/7
            array = np.zeros([7, 7], np.uint8)
            c1 = 0
            c2 = 0
            for i in range(0,300-a1,a1):
                a+=a1
                c2 = 0
                for j in range(0,300-b1, b1):
                    cx = int(i + (300/14))
                    cy = int(j + (300/14))
                    if gray_dst[cy, cx] == 255:
                        array[c2,c1] = 1
                    b+=b1
                    c2+=1
                c1+=1
            s = marker_id(array)
            if s == 152:
                array = np.fliplr(array)
                pts1 = np.float32([pt[1], pt[0], pt[3], pt[2]])
            elif s == 831:
                array = np.rot90(array)
                pts1 = np.float32([pt[1], pt[2], pt[3], pt[0]])
                
            elif s == 1011:
                array = np.rot90(array, 3)
                pts1 = np.float32([pt[3], pt[0], pt[1], pt[2]])
            elif s == 200:
                pass
            
            else:
                print ("Invalid Marker")
            M = cv2.getPerspectiveTransform(pts1,pts2)
            dst = cv2.warpPerspective(org,M,(300,300))
            gray_dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
            ret2,gray_dst = cv2.threshold(gray_dst,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
##            print objp
##            print pts1
            pts1 = pts1.reshape(4,1,2)
            _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, pts1, mtx, dist)
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
            img = draw(img,pts1,imgpts)

            
            print (ids)
            print (array)
            cv2.imshow('gray_dst', gray_dst)

            cv2.imshow('dst', dst)
##    cv2.imshow('cnt', cont)
##    cv2.imshow('gray', gray)
    cv2.imshow('auto', auto)
    cv2.imshow('img', img)
    ##cv2.imshow('edge', auto)
    if cv2.waitKey(1) == 27:
        break
print (ids)
s = marker_id(array)
print (s)
cv2.destroyAllWindows()
cap.release()
